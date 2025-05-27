import requests

def init_elasticsearch_data():
    es_url = "http://localhost:9200/products/_doc"

    products = [
        {"name": "청바지 남성용"},
        {"name": "청바지 여성용"},
        {"name": "흰색 티셔츠"},
        {"name": "스마트폰 케이스"},
        {"name": "갈색 가방"},
        {"name": "노트북 거치대"},
        {"name": "운동화"},
        {"name": "선글라스"},
        {"name": "무선 이어폰"}
    ]

    for product in products:
        res = requests.post(es_url, json=product)
        print(res.json())

if __name__ == "__main__":
    init_elasticsearch_data()