from fastapi import APIRouter, Query, HTTPException, Cookie, Depends
from pydantic import BaseModel
import requests
import sqlite3
from jose import jwt, JWTError
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
es = Elasticsearch("http://localhost:9200",
                   headers={
                       "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
                       "Content-Type": "application/vnd.elasticsearch+json; compatible-with=8"
                   })
router = APIRouter()

# JWT 설정
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# 사용자 인증 함수
def get_user_email(session_id: str = Cookie(None)) -> str:
    if not session_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    try:
        payload = jwt.decode(session_id, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=401, detail="이메일이 포함되지 않음")
        return user_email
    except JWTError:
        raise HTTPException(status_code=401, detail="세션이 만료되었거나 유효하지 않음")


@router.get("/")
def search_product(keyword: str = Query(..., description="검색 키워드")):
    keywords = [kw.strip() for kw in keyword.replace(",", " ").split() if kw.strip()]
    if not keywords:
        return {"results": []}

    should_clauses = [
        {
            "multi_match": {
                "query": kw,
                "fields": ["title", "main_category", "middle_category", "text_description"]
            }
        }
        for kw in keywords
    ]

    query = {
        "query": {
            "bool": {
                "should": should_clauses,
                "minimum_should_match": 1  # 최소 한 단어 이상 포함된 결과 반환
            }
        },
        "_source": ["title", "price", "image", "url"],
        "size": 100
    }

    try:
        result = es.search(index="products", body=query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    products = [
        {
            "id": hit["_id"],
            **hit["_source"]
        }
        for hit in result["hits"]["hits"]
    ]

    return {"results": products}


class AddToCartRequest(BaseModel):
    product_name: str
    quantity: int

@router.get("/products")
def get_products(id: str = Query(..., description="상품 ID"),
                 session_id: str = Cookie(default=None)):
    try:
        doc = es.get(index="products", id=id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
    source = doc.get("_source", {})

    user_email = None
    if session_id:
        try:
            payload = jwt.decode(session_id, SECRET_KEY, algorithms=[ALGORITHM])
            user_email = payload.get("sub")

        except JWTError:
            raise HTTPException(status_code=401, detail="유효하지 않은 세션입니다.")
    title = source.get("title")

    if user_email and title:
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            # UPSERT (기존에 있으면 UPDATE, 없으면 INSERT)
            cursor.execute("""
                INSERT INTO user_clicks (user_email, last_clicked_name)
                VALUES (?, ?)
                ON CONFLICT(user_email) DO UPDATE SET
                    last_clicked_name=excluded.last_clicked_name,
                    timestamp=CURRENT_TIMESTAMP
            """, (user_email, title))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[오류] 클릭 정보 저장 실패: {e}")
    product = {
        "id": doc["_id"],
        "title": title,
        "price": source.get("price"),
        "url": source.get("url"),
        "image_url": source.get("image"),
        "text_description": source.get("text_description"),
        "image_description": source.get("image_description"),
    }

    return product


