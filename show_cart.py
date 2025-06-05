from fastapi import APIRouter, HTTPException, Cookie, Depends, Query
import sqlite3
from jose import jwt, JWTError
from elasticsearch import Elasticsearch
router = APIRouter()
from fastapi.responses import JSONResponse
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

# ✅ 장바구니 목록 조회
@router.get("/items")
def get_cart_items(user_email: str = Depends(get_user_email)):
    es = Elasticsearch("http://localhost:9200",
                       headers={
                           "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
                           "Content-Type": "application/vnd.elasticsearch+json; compatible-with=8"
                       })
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT product_id FROM cart_items WHERE user_email = ?",
        (user_email,)
    )
    items = cursor.fetchall()
    conn.close()
    product_ids = [item[0] for item in items]

    if not product_ids:
        return JSONResponse(content=[], status_code=200)
    res = es.mget(index="products", body={"ids": product_ids})
    docs = [{
        "id":doc["_id"],
        **doc["_source"]
        }
        for doc in res["docs"] if doc["found"]
    ]
    return {"results":docs}

@router.post("/item/{id}")
def add_cart_item(id: str , user_email: str = Depends(get_user_email)):
    try:
        conn = sqlite3.connect("users.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cart_items (user_email, product_id) VALUES (?, ?)",
            (user_email, id)
        )
        conn.commit()
        conn.close()
        return {"message": f"장바구니에 추가했습니다."}

    except:
        raise HTTPException(status_code=400, detail="이미 장바구니에 추가된 상품입니다.")

# ✅ 장바구니에서 물품 제거 (수량 지정 가능)
@router.delete("/item/{id}")
def remove_cart_item(
    id: str ,
    user_email: str = Depends(get_user_email)
):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()


    cursor.execute(
            "DELETE FROM cart_items WHERE user_email = ? AND product_id = ?",
            (user_email, id)
    )

    conn.commit()
    conn.close()

    return {"message": " 장바구니에서 제거했습니다."}