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



# 전체 상품 목록 가져오기
def fetch_products():
    res = requests.get("http://localhost:9200/products/_search", json={"size": 1000})
    return res.json().get("hits", {}).get("hits", [])

# 이름으로 상품 정보 가져오기
def fetch_product_by_name(title: str):
    query = {
        "query": {
            "match": {
                "title": title
            }
        }
    }
    res = requests.get("http://localhost:9200/products/_search", json=query)
    hits = res.json().get("hits", {}).get("hits", [])
    if not hits:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
    return hits[0]["_source"]

# 유사 상품 추천
@router.get("/")
def recommend(
    session_id: str = Cookie(default=None),
    product_name: str = Query(None, description="선택적으로 클릭한 상품 이름"),
    top_n: int = 8
):
    clicked_rows=None
    if session_id:
        try:
            payload = jwt.decode(session_id, SECRET_KEY, algorithms=[ALGORITHM])
            user_email = payload.get("sub")
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT last_clicked_name FROM user_clicks WHERE user_email = ?
                """, (user_email,))
            conn.commit()
            clicked_rows = cursor.fetchall()
            conn.close()
        except JWTError:
            raise HTTPException(status_code=401, detail="유효하지 않은 세션입니다.")

    all_docs = fetch_products()

    if product_name:
        # 상품 하나 기준 추천
        base_product = fetch_product_by_name(product_name)
        base_description = base_product.get("text_description", "")
        descriptions = [base_description] + [doc["_source"].get("text_description", "") for doc in all_docs]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        top_indices = cosine_sim.argsort()[::-1][:top_n]
        recommendations = [
            {
                **all_docs[i]["_source"],
                "id": all_docs[i]["_id"]
            }
            for i in top_indices
        ]
        return {
            "base_product": product_name,
            "recommendations": recommendations
        }


    default = [
        {
            **all_docs[i]["_source"],
            "id": all_docs[i]["_id"]
        }
        for i in range(top_n)
    ]
    if not clicked_rows:
        return {
            "base_product": "기본 추천",
            "recommendations": default
        }

    clicked_names = [row[0] for row in clicked_rows]
    clicked_descriptions = []
    for title in clicked_names:
        try:
            product = fetch_product_by_name(title)
            clicked_descriptions.append(product.get("description", ""))
        except:
            continue

    if not clicked_descriptions:
        return {
            "base_product": "기본 추천",
            "recommendations": default
        }

    # 평균 벡터 기반 추천
    descriptions = clicked_descriptions + [doc["_source"].get("text_description", "") for doc in all_docs]
    descriptions = [desc if desc is not None else "" for desc in descriptions]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    mean_vector = tfidf_matrix[:len(clicked_descriptions)].mean(axis=0).A1
    cosine_sim = cosine_similarity([mean_vector], tfidf_matrix[len(clicked_descriptions):]).flatten()
    top_indices = cosine_sim.argsort()[::-1][:top_n]
    recommendations = [
        {
            **all_docs[i]["_source"],
            "id": all_docs[i]["_id"]
        }
        for i in top_indices
    ]

    return {
        "base_product": "최근 클릭 상품 기반",
        "clicked_products": clicked_names,
        "recommendations": recommendations
    }

