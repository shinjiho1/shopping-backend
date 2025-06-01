from fastapi import APIRouter, HTTPException, Cookie, Query
from jose import jwt, JWTError
import requests
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()

# JWT 설정
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# 기본 추천 상품
DEFAULT_ITEMS = ["데님 트러커 자켓", "벤큐 게이밍 모니터", "삼다수 생수 2L"]

# 전체 상품 목록 가져오기
def fetch_products():
    res = requests.get("http://localhost:9200/products/_search", json={"size": 1000})
    return res.json().get("hits", {}).get("hits", [])

# 이름으로 상품 정보 가져오기
def fetch_product_by_name(name: str):
    query = {
        "query": {
            "match": {
                "name": name
            }
        }
    }
    res = requests.get("http://localhost:9200/products/_search", json=query)
    hits = res.json().get("hits", {}).get("hits", [])
    if not hits:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
    return hits[0]["_source"]

# 유사 상품 추천
@router.get("/recommend")
def recommend(
    session_id: str = Cookie(default=None),
    product_name: str = Query(None, description="선택적으로 클릭한 상품 이름"),
    top_n: int = 3
):
    try:
        # 로그인 여부 확인
        payload = jwt.decode(session_id, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")

        all_docs = fetch_products()

        if product_name:
            # 상품 하나 기준 추천
            base_product = fetch_product_by_name(product_name)
            base_description = base_product.get("description", "")
            descriptions = [base_description] + [doc["_source"].get("description", "") for doc in all_docs]
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(descriptions)
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            top_indices = cosine_sim.argsort()[::-1][:top_n]
            recommendations = [all_docs[i]["_source"]["name"] for i in top_indices]
            return {
                "base_product": product_name,
                "recommendations": recommendations
            }

        # 클릭한 상품들로 추천 (벡터 평균)
        conn = sqlite3.connect("shopping.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_clicks (
            user_email TEXT,
            last_clicked_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        clicked_rows = cursor.fetchall()
        conn.close()

        if not clicked_rows:
            return {
                "base_product": "기본 추천",
                "recommendations": DEFAULT_ITEMS[:top_n]
            }

        clicked_names = [row[0] for row in clicked_rows]
        clicked_descriptions = []
        for name in clicked_names:
            try:
                product = fetch_product_by_name(name)
                clicked_descriptions.append(product.get("description", ""))
            except:
                continue

        if not clicked_descriptions:
            return {
                "base_product": "기본 추천",
                "recommendations": DEFAULT_ITEMS[:top_n]
            }

        # 평균 벡터 기반 추천
        descriptions = clicked_descriptions + [doc["_source"].get("description", "") for doc in all_docs]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        mean_vector = tfidf_matrix[:len(clicked_descriptions)].mean(axis=0)
        cosine_sim = cosine_similarity(mean_vector, tfidf_matrix[len(clicked_descriptions):]).flatten()
        top_indices = cosine_sim.argsort()[::-1][:top_n]
        recommendations = [all_docs[i]["_source"]["name"] for i in top_indices]

        return {
            "base_product": "최근 클릭 상품 기반",
            "clicked_products": clicked_names,
            "recommendations": recommendations
        }

    except JWTError:
        # 비회원일 경우
        return {
            "base_product": "기본 추천",
            "recommendations": DEFAULT_ITEMS[:top_n]
        }