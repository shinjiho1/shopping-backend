from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 각 기능 라우터 import
from login_system import router as login_router
from search_product import router as search_router
from product_recommend import router as recommend_router
from select_category import router as category_router
from show_cart import router as cart_router

app = FastAPI()

# CORS 설정 (프론트랑 연결할 때 필요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포 시 도메인 제한 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(login_router, prefix="/auth")
app.include_router(search_router, prefix="/search")
app.include_router(recommend_router, prefix="/recommend")
app.include_router(category_router, prefix="/category")
app.include_router(cart_router, prefix="/cart")