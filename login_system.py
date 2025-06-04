from fastapi import APIRouter, HTTPException, Response, Cookie
from pydantic import BaseModel, EmailStr, validator
import sqlite3
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from email_validator import validate_email, EmailNotValidError
from fastapi.responses import JSONResponse
router = APIRouter()

# JWT 설정
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# DB 초기화
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            product_id TEXT NOT NULL,
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_clicks (
            user_email TEXT Primary key,
            last_clicked_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
        """)
    conn.commit()
    conn.close()

init_db()

# 회원가입용 모델
class RegisterUser(BaseModel):
    email: str
    password: str
    confirm_password: str

    @validator("email", pre=True, always=True)
    def validate_email_format(cls, v):
        try:
            validate_email(v)
        except ValueError:
            raise HTTPException(status_code=422, detail="이메일 형식이 올바르지 않습니다.")
        return v
    @validator("confirm_password", pre=True, always=True)
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return v

# 로그인용 모델
class LoginUser(BaseModel):
    email: EmailStr
    password: str

# JWT 생성 함수
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 루트 상태 확인
@router.get("/")
def read_root():
    return {"message": "서버가 정상 작동 중입니다."}

# 회원가입 API
@router.post("/register")
def register(user: RegisterUser):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (user.email, hashed_pw.decode('utf-8')))
    conn.commit()
    conn.close()

    return {"message": "회원가입 성공!"}

# 로그인 API
@router.post("/login")
def login(user: LoginUser, response: Response):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE email = ?", (user.email,))
    result = cursor.fetchone()

    if result and bcrypt.checkpw(user.password.encode('utf-8'), result[0].encode('utf-8')):
        access_token = create_access_token(data={"sub": user.email})
        response = JSONResponse(content={
            "message": f"{user.email}님 환영합니다!",

        })
        response.set_cookie(
            key="session_id",
            value=access_token,
            httponly=True,
            samesite="lax",
            secure=False
        )
        return response
    else:
        conn.close()
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 틀렸습니다.")

# 보호된 API
@router.get("/protected")
def protected(session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    try:
        payload = jwt.decode(session_id, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        return {"message": f"{user_email}님의 장바구니를 불러왔습니다!"}
    except JWTError:
        raise HTTPException(status_code=401, detail="세션이 만료되었거나 유효하지 않습니다.")

# 로그아웃 API
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="session_id",
        httponly=True,
        samesite="lax",
        path="/"
    )
    return {"message": "로그아웃 되었습니다."}