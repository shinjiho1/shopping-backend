from fastapi import APIRouter, Query, HTTPException, Cookie, Depends
from pydantic import BaseModel
import requests
import sqlite3
from jose import jwt, JWTError

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

# ✅ 상품 검색 API (product_id 제거)
@router.get("/product/search")
def search_product(keyword: str = Query(..., description="검색 키워드")):
    es_url = "http://localhost:9200/products/_search"
    query = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["name", "main_category", "sub_category", "brand", "description"]
            }
        }
    }
    response = requests.get(es_url, json=query)
    result = response.json()

    hits = result.get("hits", {}).get("hits", [])
    products = [
        {
            "name": doc["_source"].get("name"),
            "price": doc["_source"].get("price"),
            "url": doc["_source"].get("url"),
            "main_category": doc["_source"].get("main_category"),
            "sub_category": doc["_source"].get("sub_category"),
            "brand": doc["_source"].get("brand"),
            "image": doc["_source"].get("image"),
            "description": doc["_source"].get("description")
        }
        for doc in hits
    ]

    if products:
        return {"results": products}
    return {"message": "검색 결과 없음"}

# ✅ 장바구니 요청 데이터 (name 기준)
class AddToCartRequest(BaseModel):
    product_name: str
    quantity: int

# ✅ 장바구니 추가 API (Elasticsearch에서 이름으로 확인)
@router.post("/product/cart")
def add_to_cart(item: AddToCartRequest, user_email: str = Depends(get_user_email)):
    es_url = "http://localhost:9200/products/_search"
    query = {
        "query": {
            "match": {
                "name": item.product_name
            }
        }
    }
    es_response = requests.get(es_url, json=query)
    hits = es_response.json().get("hits", {}).get("hits", [])

    if not hits:
        raise HTTPException(status_code=404, detail="존재하지 않는 상품입니다.")

    # SQLite에 장바구니 저장
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT quantity FROM cart_items WHERE user_email = ? AND product_id = ?",
        (user_email, item.product_name)
    )
    row = cursor.fetchone()

    if row:
        new_qty = row[0] + item.quantity
        cursor.execute(
            "UPDATE cart_items SET quantity = ? WHERE user_email = ? AND product_id = ?",
            (new_qty, user_email, item.product_name)
        )
    else:
        cursor.execute(
            "INSERT INTO cart_items (user_email, product_id, quantity) VALUES (?, ?, ?)",
            (user_email, item.product_name, item.quantity)
        )

    conn.commit()
    conn.close()

    return {"message": f"{item.product_name}가 장바구니에 추가되었습니다."}