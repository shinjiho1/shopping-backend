from fastapi import APIRouter, HTTPException, Cookie, Depends, Query
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

# ✅ 장바구니 목록 조회
@router.get("/items")
def get_cart_items(user_email: str = Depends(get_user_email)):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT product_id, quantity FROM cart_items WHERE user_email = ?",
        (user_email,)
    )
    items = cursor.fetchall()
    conn.close()
    return {"cart": [{"product_name": name, "quantity": qty} for name, qty in items]}

# ✅ 장바구니에서 물품 제거 (수량 지정 가능)
@router.delete("/item/{product_name}")
def remove_cart_item(
    product_name: str,
    quantity: int = Query(..., gt=0, description="제거할 수량"),
    user_email: str = Depends(get_user_email)
):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # 현재 수량 확인
    cursor.execute(
        "SELECT quantity FROM cart_items WHERE user_email = ? AND product_id = ?",
        (user_email, product_name)
    )
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="장바구니에 해당 상품이 없습니다.")

    current_qty = row[0]
    if quantity >= current_qty:
        # 전부 제거
        cursor.execute(
            "DELETE FROM cart_items WHERE user_email = ? AND product_id = ?",
            (user_email, product_name)
        )
    else:
        # 일부만 감소
        cursor.execute(
            "UPDATE cart_items SET quantity = ? WHERE user_email = ? AND product_id = ?",
            (current_qty - quantity, user_email, product_name)
        )

    conn.commit()
    conn.close()

    return {"message": f"{product_name} {quantity}개를 장바구니에서 제거했습니다."}