from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "서버가 정상 작동 중입니다."}

# DB 초기화
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            realname TEXT NOT NULL,
            phonenumber TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()  

# 사용자 모델 
class User(BaseModel):
    username: str
    password: str
    realname: str
    phonenumber: str 

# 회원가입
@app.post("/register")
def register(user: User):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # 사용자 중복 확인
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")

    # 사용자 등록
    cursor.execute("""INSERT INTO users (username, password, realname, phonenumber) 
                   VALUES (?, ?, ?, ?)
                   """, (user.username, user.password, user.realname, user.phonenumber))
    conn.commit()
    conn.close()
    return {"message": "회원가입 성공!"}

# 로그인
@app.post("/login")
def login(user: User):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user.username, user.password))
    result = cursor.fetchone()
    conn.close()

    if result:
        return {"message": f"환영합니다, {user.username}님!"}
    else:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸습니다.")