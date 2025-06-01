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

@router.get("/category")
def get_products_by_category(
    main_category: str = Query(..., description="대분류 예: 의류, 전자제품, 가공식품, 책, 신발"),
    sub_category: Optional[str] = Query(None, description="소분류 예: 상의, 하의 등")
):
    # 검색 조건 구성
    must_conditions = [{"match": {"main_category": main_category}}]
    if sub_category:
        must_conditions.append({"match": {"sub_category": sub_category}})

    # ES 조회
    response = es.search(
        index="products",
        body={
            "query": {
                "bool": {
                    "must": must_conditions
                }
            },
            "_source": ["name", "price", "main_category", "sub_category", "image", "url", "brand", "description"],
            "size": 100
        }
    )

    # 상품 결과
    products = [hit["_source"] for hit in response["hits"]["hits"]]

    # 소분류 목록만 추출 (sub_category가 없을 때만)
    subcategories = []
    if not sub_category:
        sub_response = es.search(
            index="products",
            body={
                "query": {
                    "match": {
                        "main_category": main_category
                    }
                },
                "_source": ["sub_category"],
                "size": 100
            }
        )
        subcategories = list(set(hit["_source"]["sub_category"] for hit in sub_response["hits"]["hits"] if "sub_category" in hit["_source"]))

    return {
        "main_category": main_category,
        "sub_category": sub_category,
        "subcategories": subcategories if not sub_category else [],
        "products": products
    }