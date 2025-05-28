from fastapi import FastAPI
from login_system import app as login_app
from search_product import app as search_app
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 프론트 도메인
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST 등 모든 HTTP 메서드 허용
    allow_headers=["*"],     # 모든 헤더 허용
)

@app.get("/")
def read_root():
    return {"message": "서버가 정상 작동 중입니다."}
# 라우팅 통합
app.mount("/auth", login_app)
app.mount("/shop", search_app)