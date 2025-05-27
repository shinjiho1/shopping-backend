from fastapi import FastAPI, Query, HTTPException, Cookie, Depends
from pydantic import BaseModel
import requests
import sqlite3
from jose import jwt, JWTError

app = FastAPI()

# JWT 설정 (로그인된 사용자 인증용)
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# ✅ 사용자 인증 함수
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

# ✅ 상품 검색 API (GET /search)
@app.get("/search")
def search_product(keyword: str = Query(..., description="검색 키워드")):
    es_url = "http://localhost:9200/products/_search"
    query = {
        "query": {
            "match": {
                "name": keyword
            }
        }
    }
    response = requests.get(es_url, json=query)
    result = response.json()

    hits = result.get("hits", {}).get("hits", [])
    products = [{"product_id": doc["_id"], **doc["_source"]} for doc in hits]

    if products:
        return {"results": products}
    return {"message": "검색 결과 없음"}

# ✅ 장바구니 추가 요청 데이터 모델
class AddToCartRequest(BaseModel):
    product_id: str
    quantity: int

# ✅ 장바구니 추가 API (POST /cart)
@app.post("/cart")
def add_to_cart(item: AddToCartRequest, user_email: str = Depends(get_user_email)):
    # 1. Elasticsearch에서 상품 존재 확인
    es_url = f"http://localhost:9200/products/_doc/{item.product_id}"
    es_response = requests.get(es_url)

    if es_response.status_code != 200:
        raise HTTPException(status_code=404, detail="존재하지 않는 상품입니다.")

    # 2. SQLite DB 연결
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # 3. cart_items 테이블에 같은 상품이 있는지 확인
    cursor.execute(
        "SELECT quantity FROM cart_items WHERE user_email = ? AND product_id = ?",
        (user_email, item.product_id)
    )
    row = cursor.fetchone()

    if row:
        # 이미 있으면 수량만 증가
        new_qty = row[0] + item.quantity
        cursor.execute(
            "UPDATE cart_items SET quantity = ? WHERE user_email = ? AND product_id = ?",
            (new_qty, user_email, item.product_id)
        )
    else:
        # 없으면 새로 삽입
        cursor.execute(
            "INSERT INTO cart_items (user_email, product_id, quantity) VALUES (?, ?, ?)",
            (user_email, item.product_id, item.quantity)
        )

    conn.commit()
    conn.close()

    return {"message": f"상품 {item.product_id}가 장바구니에 추가되었습니다."}