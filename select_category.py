from fastapi import APIRouter, Query
from typing import Optional
from elasticsearch import Elasticsearch

router = APIRouter()

# Elasticsearch 클라이언트 (v8 호환 헤더 포함)
es = Elasticsearch(
    "http://localhost:9200",
    headers={
        "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
        "Content-Type": "application/vnd.elasticsearch+json; compatible-with=8"
    }
)

@router.get("/")
def get_products_by_category(
    type: str = Query(..., description="대분류 예: 의류, 전자제품, 가공식품, 책, 신발"),
    category: Optional[str] = Query(None, description="소분류 예: 상의, 하의 등")
):
    # 검색 조건 구성
    must_conditions = [{"match": {"main_category": type}}]
    if category:
        must_conditions.append({"match": {"middle_category": category}})

    # ES 조회
    response = es.search(
        index="products",
        body={
            "query": {
                "bool": {
                    "must": must_conditions
                }
            },
            "_source": ["title", "price", "image", "url"],
            "size": 100
        }
    )

    # 상품 결과
    products = [
        {
            "id": hit["_id"],
            **hit["_source"]
        }
        for hit in response["hits"]["hits"]
    ]


    return {"products": products}