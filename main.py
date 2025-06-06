from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from login_system import init_db
# 각 기능 라우터 import
from login_system import router as login_router
from search_product import router as search_router
from product_recommend import router as recommend_router
from select_category import router as category_router
from show_cart import router as cart_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],  # 프론트 도메인
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST 등 모든 HTTP 메서드 허용
    allow_headers=["*"],     # 모든 헤더 허용
)

@app.get("/")
def read_root():
    init_db()
    return {"message": "서버가 정상 작동 중입니다."}
# 라우팅 통합

# 라우터 등록
app.include_router(login_router, prefix="/auth")
app.include_router(search_router, prefix="/search")
app.include_router(recommend_router, prefix="/recommend")
app.include_router(category_router, prefix="/category")
app.include_router(cart_router, prefix="/cart")