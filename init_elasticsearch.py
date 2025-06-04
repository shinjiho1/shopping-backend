import requests

def init_elasticsearch_data():
        es_url = "http://localhost:9200/products/_doc"

        products = [
             {
            "name": "경량 패딩 자켓",
            "price": 59000,
            "url": "http://example.com/product/outer1",
            "main_category": "의류",
            "sub_category": "아우터",
            "image": "http://example.com/image/outer1.jpg",
            "description": "가볍고 따뜻한 경량 패딩으로 일상복이나 아웃도어에 적합합니다.",
            "brand": "노스페이스"
            },
            {
            "name": "블랙 롱코트",
            "price": 129000,
            "url": "http://example.com/product/outer2",
            "main_category": "의류",
            "sub_category": "아우터",
            "image": "http://example.com/image/outer2.jpg",
            "description": "겨울철 비즈니스룩에 어울리는 고급스러운 롱코트입니다.",
            "brand": "지오다노"
            },
            {
            "name": "데님 트러커 자켓",
            "price": 47000,
            "url": "http://example.com/product/outer3",
            "main_category": "의류",
            "sub_category": "아우터",
            "image": "http://example.com/image/outer3.jpg",
            "description": "빈티지 스타일의 데님 자켓으로 봄/가을용으로 적합합니다.",
            "brand": "리바이스"
            },
             {
            "name": "기본 흰색 반팔 티셔츠",
            "price": 15000,
            "url": "http://example.com/product/top1",
            "main_category": "의류",
            "sub_category": "상의",
            "image": "http://example.com/image/top1.jpg",
            "description": "편하게 입을 수 있는 면 소재의 흰색 반팔 티셔츠입니다.",
            "brand": "유니클로"
            },
            {
            "name": "스트라이프 셔츠",
            "price": 39000,
            "url": "http://example.com/product/top2",
            "main_category": "의류",
            "sub_category": "상의",
            "image": "http://example.com/image/top2.jpg",
            "description": "클래식한 스트라이프 디자인의 긴팔 셔츠입니다.",
            "brand": "지오다노"
        },
        {
            "name": "후드 풀오버",
            "price": 49000,
            "url": "http://example.com/product/top3",
            "main_category": "의류",
            "sub_category": "상의",
            "image": "http://example.com/image/top3.jpg",
            "description": "편안한 핏의 후드 풀오버로 일상복이나 운동복으로 적합합니다.",
            "brand": "나이키"
        },
        {
            "name": "블랙 슬림핏 청바지",
            "price": 45000,
            "url": "http://example.com/product/bottom1",
            "main_category": "의류",
            "sub_category": "하의",
            "image": "http://example.com/image/bottom1.jpg",
            "description": "스타일리시한 블랙 슬림핏 데님 팬츠입니다.",
            "brand": "리바이스"
        },
        {
            "name": "그레이 조거팬츠",
            "price": 32000,
            "url": "http://example.com/product/bottom2",
            "main_category": "의류",
            "sub_category": "하의",
            "image": "http://example.com/image/bottom2.jpg",
            "description": "편안한 착용감을 제공하는 캐주얼 조거팬츠입니다.",
            "brand": "아디다스"
        },
        {
            "name": "면 반바지",
            "price": 27000,
            "url": "http://example.com/product/bottom3",
            "main_category": "의류",
            "sub_category": "하의",
            "image": "http://example.com/image/bottom3.jpg",
            "description": "여름철에 입기 좋은 시원한 면 소재 반바지입니다.",
            "brand": "스파오"
        },
        {
            "name": "코튼 체크 파자마 세트",
            "price": 38000,
            "url": "http://example.com/product/homewear1",
            "main_category": "의류",
            "sub_category": "홈웨어",
            "image": "http://example.com/image/homewear1.jpg",
            "description": "부드러운 면 소재의 체크 무늬 파자마 세트입니다.",
            "brand": "유니클로"
        },
        {
            "name": "여성용 실크 슬립웨어",
            "price": 59000,
            "url": "http://example.com/product/homewear2",
            "main_category": "의류",
            "sub_category": "홈웨어",
            "image": "http://example.com/image/homewear2.jpg",
            "description": "고급스러운 실크 소재의 여성용 슬립웨어입니다.",
            "brand": "비비안"
        },
        {
            "name": "남성 기모 라운지웨어",
            "price": 42000,
            "url": "http://example.com/product/homewear3",
            "main_category": "의류",
            "sub_category": "홈웨어",
            "image": "http://example.com/image/homewear3.jpg",
            "description": "추운 날씨에도 따뜻한 기모 라운지웨어 세트입니다.",
            "brand": "탑텐"
        },
         {
        "name": "남성 기능성 드로즈",
        "price": 12900,
        "url": "http://example.com/product/underwear1",
        "main_category": "의류",
        "sub_category": "언더웨어",
        "image": "http://example.com/image/underwear1.jpg",
        "description": "뛰어난 통기성과 편안한 착용감을 제공하는 남성 기능성 드로즈입니다.",
        "brand": "BYC"
    },
    {
        "name": "여성 레이스 브라렛",
        "price": 18900,
        "url": "http://example.com/product/underwear2",
        "main_category": "의류",
        "sub_category": "언더웨어",
        "image": "http://example.com/image/underwear2.jpg",
        "description": "편안한 착용감과 세련된 디자인이 돋보이는 여성 레이스 브라렛입니다.",
        "brand": "비비안"
    },
    {
        "name": "아동 순면 팬티 3매입",
        "price": 8900,
        "url": "http://example.com/product/underwear3",
        "main_category": "의류",
        "sub_category": "언더웨어",
        "image": "http://example.com/image/underwear3.jpg",
        "description": "부드러운 면 소재로 제작된 아동용 팬티 3종 세트입니다.",
        "brand": "유니클로"
    },
        {
            "name": "LG 27인치 모니터",
            "price": 270000,
            "url": "http://example.com/product/tv1",
            "main_category": "전자제품",
            "sub_category": "TV/모니터",
            "image": "http://example.com/image/tv1.jpg",
            "description": "LG의 고해상도 IPS 27인치 모니터입니다.",
            "brand": "LG"
        },
        {
            "name": "삼성 스마트TV 55인치",
            "price": 820000,
            "url": "http://example.com/product/tv2",
            "main_category": "전자제품",
            "sub_category": "TV/모니터",
            "image": "http://example.com/image/tv2.jpg",
            "description": "삼성 QLED 기술의 4K 스마트TV입니다.",
            "brand": "삼성"
        },
        {
            "name": "벤큐 게이밍 모니터",
            "price": 350000,
            "url": "http://example.com/product/tv3",
            "main_category": "전자제품",
            "sub_category": "TV/모니터",
            "image": "http://example.com/image/tv3.jpg",
            "description": "벤큐의 144Hz 지원 게이밍 전용 모니터입니다.",
            "brand": "BenQ"
        },
        {
            "name": "애플 맥북 에어 M2",
            "price": 1450000,
            "url": "http://example.com/product/it1",
            "main_category": "전자제품",
            "sub_category": "IT기기",
            "image": "http://example.com/image/it1.jpg",
            "description": "Apple M2 칩이 탑재된 초경량 맥북입니다.",
            "brand": "Apple"
        },
        {
            "name": "삼성 갤럭시 탭 S9",
            "price": 980000,
            "url": "http://example.com/product/it2",
            "main_category": "전자제품",
            "sub_category": "IT기기",
            "image": "http://example.com/image/it2.jpg",
            "description": "갤럭시 탭 S9의 고성능 안드로이드 태블릿.",
            "brand": "삼성"
        },
        {
            "name": "레노버 아이디어패드",
            "price": 730000,
            "url": "http://example.com/product/it3",
            "main_category": "전자제품",
            "sub_category": "IT기기",
            "image": "http://example.com/image/it3.jpg",
            "description": "학생과 직장인을 위한 가성비 좋은 노트북입니다.",
            "brand": "Lenovo"
        },
        {
            "name": "LG 디오스 냉장고",
            "price": 1650000,
            "url": "http://example.com/product/fridge1",
            "main_category": "전자제품",
            "sub_category": "냉장고",
            "image": "http://example.com/image/fridge1.jpg",
            "description": "신선함을 오래 유지하는 LG 디오스 냉장고.",
            "brand": "LG"
        },
        {
            "name": "삼성 비스포크 냉장고",
            "price": 1780000,
            "url": "http://example.com/product/fridge2",
            "main_category": "전자제품",
            "sub_category": "냉장고",
            "image": "http://example.com/image/fridge2.jpg",
            "description": "인테리어에 맞춘 모듈형 디자인의 냉장고.",
            "brand": "삼성"
        },
        {
            "name": "위니아 소형 냉장고",
            "price": 480000,
            "url": "http://example.com/product/fridge3",
            "main_category": "전자제품",
            "sub_category": "냉장고",
            "image": "http://example.com/image/fridge3.jpg",
            "description": "1인 가구에 적합한 컴팩트 냉장고.",
            "brand": "위니아"
        },
        {
            "name": "신일 서큘레이터",
            "price": 68000,
            "url": "http://example.com/product/season1",
            "main_category": "전자제품",
            "sub_category": "계절기기",
            "image": "http://example.com/image/season1.jpg",
            "description": "강력한 바람을 제공하는 서큘레이터입니다.",
            "brand": "신일"
        },
        {
            "name": "위닉스 제습기",
            "price": 240000,
            "url": "http://example.com/product/season2",
            "main_category": "전자제품",
            "sub_category": "계절기기",
            "image": "http://example.com/image/season2.jpg",
            "description": "장마철 필수 제습기, 20L 고용량.",
            "brand": "위닉스"
        },
        {
            "name": "LG 휘센 에어컨",
            "price": 2100000,
            "url": "http://example.com/product/season3",
            "main_category": "전자제품",
            "sub_category": "계절기기",
            "image": "http://example.com/image/season3.jpg",
            "description": "AI 스마트 냉방이 가능한 스탠드형 에어컨.",
            "brand": "LG"
        },
        {
            "name": "쿠쿠 전기밥솥",
            "price": 160000,
            "url": "http://example.com/product/kitchen1",
            "main_category": "전자제품",
            "sub_category": "주방 전자제품",
            "image": "http://example.com/image/kitchen1.jpg",
            "description": "고압력 밥짓기로 맛있는 밥 완성!",
            "brand": "쿠쿠"
        },
        {
            "name": "필립스 에어프라이어",
            "price": 139000,
            "url": "http://example.com/product/kitchen2",
            "main_category": "전자제품",
            "sub_category": "주방 전자제품",
            "image": "http://example.com/image/kitchen2.jpg",
            "description": "기름 없이 바삭하게 조리하는 에어프라이어.",
            "brand": "필립스"
        },
        {
         "name": "브레빌 커피머신",
         "price": 890000,
         "url": "http://example.com/product/kitchen3",
         "main_category": "전자제품",
         "sub_category": "주방 전자제품",
         "image": "http://example.com/image/kitchen3.jpg",
         "description": "전문가용 에스프레소 커피 머신입니다.",
         "brand": "브레빌"
        },
         {
    "name": "삼다수 생수 2L",
    "price": 1200,
    "url": "http://example.com/product/water1",
    "main_category": "가공식품",
    "sub_category": "생수/탄산수",
    "image": "http://example.com/image/water1.jpg",
    "description": "제주의 깨끗한 지하수를 담은 생수.",
    "brand": "제주삼다수"
  },
  {
    "name": "스파클 탄산수 라임 500ml",
    "price": 900,
    "url": "http://example.com/product/water2",
    "main_category": "가공식품",
    "sub_category": "생수/탄산수",
    "image": "http://example.com/image/water2.jpg",
    "description": "톡 쏘는 라임향 탄산수입니다.",
    "brand": "스파클"
  },
  {
    "name": "evian 프리미엄 생수 750ml",
    "price": 2300,
    "url": "http://example.com/product/water3",
    "main_category": "가공식품",
    "sub_category": "생수/탄산수",
    "image": "http://example.com/image/water3.jpg",
    "description": "프랑스 알프스에서 온 프리미엄 생수.",
    "brand": "evian"
  },
  {
    "name": "맥심 모카골드 커피믹스",
    "price": 9800,
    "url": "http://example.com/product/coffee1",
    "main_category": "가공식품",
    "sub_category": "커피/차",
    "image": "http://example.com/image/coffee1.jpg",
    "description": "달콤한 커피믹스의 대표 브랜드.",
    "brand": "맥심"
  },
  {
    "name": "트와이닝 얼그레이 티",
    "price": 6900,
    "url": "http://example.com/product/tea1",
    "main_category": "가공식품",
    "sub_category": "커피/차",
    "image": "http://example.com/image/tea1.jpg",
    "description": "향긋한 베르가못 향의 홍차입니다.",
    "brand": "Twinings"
  },
  {
    "name": "카누 다크 로스트 아메리카노",
    "price": 11000,
    "url": "http://example.com/product/coffee2",
    "main_category": "가공식품",
    "sub_category": "커피/차",
    "image": "http://example.com/image/coffee2.jpg",
    "description": "풍부한 향의 스틱형 인스턴트 커피.",
    "brand": "카누"
  },
  {
    "name": "펩시콜라 1.5L",
    "price": 1800,
    "url": "http://example.com/product/drink1",
    "main_category": "가공식품",
    "sub_category": "음료",
    "image": "http://example.com/image/drink1.jpg",
    "description": "청량한 탄산이 매력적인 대표 음료.",
    "brand": "펩시"
  },
  {
    "name": "게토레이 레몬맛 600ml",
    "price": 1600,
    "url": "http://example.com/product/drink2",
    "main_category": "가공식품",
    "sub_category": "음료",
    "image": "http://example.com/image/drink2.jpg",
    "description": "운동 후 수분 보충에 좋은 이온음료.",
    "brand": "게토레이"
  },
  {
    "name": "솔의눈 180ml",
    "price": 1200,
    "url": "http://example.com/product/drink3",
    "main_category": "가공식품",
    "sub_category": "음료",
    "image": "http://example.com/image/drink3.jpg",
    "description": "진한 소나무 향이 느껴지는 한국 전통 음료.",
    "brand": "해태"
  },
  {
    "name": "서울우유 흰우유 1L",
    "price": 2400,
    "url": "http://example.com/product/dairy1",
    "main_category": "가공식품",
    "sub_category": "유제품",
    "image": "http://example.com/image/dairy1.jpg",
    "description": "신선한 국산 원유 100% 우유.",
    "brand": "서울우유"
  },
  {
    "name": "빙그레 바나나맛 우유",
    "price": 1300,
    "url": "http://example.com/product/dairy2",
    "main_category": "가공식품",
    "sub_category": "유제품",
    "image": "http://example.com/image/dairy2.jpg",
    "description": "달콤한 바나나향 가득한 국민 음료.",
    "brand": "빙그레"
  },
  {
    "name": "매일 요구르트 10입",
    "price": 3800,
    "url": "http://example.com/product/dairy3",
    "main_category": "가공식품",
    "sub_category": "유제품",
    "image": "http://example.com/image/dairy3.jpg",
    "description": "유산균이 살아있는 건강 요구르트.",
    "brand": "매일유업"
  },
  {
    "name": "백설 해바라기유 900ml",
    "price": 5100,
    "url": "http://example.com/product/oil1",
    "main_category": "가공식품",
    "sub_category": "기름료",
    "image": "http://example.com/image/oil1.jpg",
    "description": "고온 조리에 적합한 해바라기유.",
    "brand": "백설"
  },
  {
    "name": "오뚜기 참기름 320ml",
    "price": 7900,
    "url": "http://example.com/product/oil2",
    "main_category": "가공식품",
    "sub_category": "기름료",
    "image": "http://example.com/image/oil2.jpg",
    "description": "풍부한 고소함을 담은 참기름.",
    "brand": "오뚜기"
  },
  {
    "name": "CJ 올리브유 500ml",
    "price": 8900,
    "url": "http://example.com/product/oil3",
    "main_category": "가공식품",
    "sub_category": "기름료",
    "image": "http://example.com/image/oil3.jpg",
    "description": "샐러드와 파스타용으로 좋은 엑스트라버진 올리브오일.",
    "brand": "CJ"
  },
  {
    "name": "책의 역사",
    "price": 15800,
    "url": "http://example.com/product/book1",
    "main_category": "책",
    "sub_category": "총류",
    "image": "http://example.com/image/book1.jpg",
    "description": "고대부터 현대까지 책의 진화사를 담은 인문 교양서.",
    "brand": "민음사"
  },
  {
    "name": "도서관의 탄생",
    "price": 17200,
    "url": "http://example.com/product/book2",
    "main_category": "책",
    "sub_category": "총류",
    "image": "http://example.com/image/book2.jpg",
    "description": "세계 도서관의 역사와 문화적 배경을 탐구합니다.",
    "brand": "책세상"
  },
  {
    "name": "출판의 미래",
    "price": 13400,
    "url": "http://example.com/product/book3",
    "main_category": "책",
    "sub_category": "총류",
    "image": "http://example.com/image/book3.jpg",
    "description": "디지털 시대의 출판 산업 변화에 대해 설명합니다.",
    "brand": "한빛미디어"
  },
  {
    "name": "소크라테스 익스프레스",
    "price": 16900,
    "url": "http://example.com/product/philo1",
    "main_category": "책",
    "sub_category": "철학",
    "image": "http://example.com/image/philo1.jpg",
    "description": "고전 철학자들과 함께하는 인생 여행.",
    "brand": "어크로스"
  },
  {
    "name": "니체의 말",
    "price": 12000,
    "url": "http://example.com/product/philo2",
    "main_category": "책",
    "sub_category": "철학",
    "image": "http://example.com/image/philo2.jpg",
    "description": "니체의 통찰을 일상 속에서 되새겨보는 책.",
    "brand": "위즈덤하우스"
  },
  {
    "name": "데카르트의 방법서설",
    "price": 8700,
    "url": "http://example.com/product/philo3",
    "main_category": "책",
    "sub_category": "철학",
    "image": "http://example.com/image/philo3.jpg",
    "description": "합리주의 철학의 기초를 설명하는 고전.",
    "brand": "서해문집"
  },
  {
    "name": "종교란 무엇인가",
    "price": 14200,
    "url": "http://example.com/product/religion1",
    "main_category": "책",
    "sub_category": "종교",
    "image": "http://example.com/image/religion1.jpg",
    "description": "세계 주요 종교들의 기원과 의미를 탐구합니다.",
    "brand": "알마"
  },
  {
    "name": "기독교의 역사",
    "price": 18500,
    "url": "http://example.com/product/religion2",
    "main_category": "책",
    "sub_category": "종교",
    "image": "http://example.com/image/religion2.jpg",
    "description": "예수에서 현대 교회까지 기독교의 흐름을 설명합니다.",
    "brand": "살림"
  },
  {
    "name": "불교란 무엇인가",
    "price": 11800,
    "url": "http://example.com/product/religion3",
    "main_category": "책",
    "sub_category": "종교",
    "image": "http://example.com/image/religion3.jpg",
    "description": "붓다의 가르침과 불교 철학을 쉽게 풀어낸 입문서.",
    "brand": "불광출판사"
  },
   {
    "name": "넛지",
    "price": 13500,
    "url": "http://example.com/product/social1",
    "main_category": "책",
    "sub_category": "사회과학",
    "image": "http://example.com/image/social1.jpg",
    "description": "사람의 행동을 유도하는 똑똑한 개입의 심리학.",
    "brand": "리더스북"
  },
  {
    "name": "사피엔스",
    "price": 19800,
    "url": "http://example.com/product/social2",
    "main_category": "책",
    "sub_category": "사회과학",
    "image": "http://example.com/image/social2.jpg",
    "description": "인류의 기원과 문명의 발전사를 통찰합니다.",
    "brand": "김영사"
  },
  {
    "name": "정의란 무엇인가",
    "price": 15000,
    "url": "http://example.com/product/social3",
    "main_category": "책",
    "sub_category": "사회과학",
    "image": "http://example.com/image/social3.jpg",
    "description": "정치 철학의 핵심 개념을 쉽게 설명한 명강의.",
    "brand": "와이즈베리"
  },
  {
    "name": "코스모스",
    "price": 21000,
    "url": "http://example.com/product/science1",
    "main_category": "책",
    "sub_category": "자연과학",
    "image": "http://example.com/image/science1.jpg",
    "description": "칼 세이건이 안내하는 우주와 과학 이야기.",
    "brand": "사이언스북스"
  },
  {
    "name": "시간은 흐르지 않는다",
    "price": 14800,
    "url": "http://example.com/product/science2",
    "main_category": "책",
    "sub_category": "자연과학",
    "image": "http://example.com/image/science2.jpg",
    "description": "물리학자가 시간의 본질을 탐구한 도전적인 과학서.",
    "brand": "쌤앤파커스"
  },
  {
    "name": "양자역학의 세계",
    "price": 16200,
    "url": "http://example.com/product/science3",
    "main_category": "책",
    "sub_category": "자연과학",
    "image": "http://example.com/image/science3.jpg",
    "description": "현대 물리학의 핵심 개념인 양자역학을 설명합니다.",
    "brand": "동아시아"
  },
   {
    "name": "나이키 에어맥스 90",
    "price": 129000,
    "url": "http://example.com/product/sneaker1",
    "main_category": "신발",
    "sub_category": "스니커즈",
    "image": "http://example.com/image/sneaker1.jpg",
    "description": "편안한 착화감과 뛰어난 쿠셔닝을 제공하는 나이키 대표 스니커즈.",
    "brand": "나이키"
  },
  {
    "name": "아디다스 슈퍼스타",
    "price": 109000,
    "url": "http://example.com/product/sneaker2",
    "main_category": "신발",
    "sub_category": "스니커즈",
    "image": "http://example.com/image/sneaker2.jpg",
    "description": "클래식한 디자인의 아디다스 대표 스니커즈.",
    "brand": "아디다스"
  },
  {
    "name": "컨버스 척테일러",
    "price": 69000,
    "url": "http://example.com/product/sneaker3",
    "main_category": "신발",
    "sub_category": "스니커즈",
    "image": "http://example.com/image/sneaker3.jpg",
    "description": "스트리트 스타일에 어울리는 유니섹스 캔버스 스니커즈.",
    "brand": "컨버스"
  },
  {
    "name": "노스페이스 다운 부츠",
    "price": 85000,
    "url": "http://example.com/product/padding1",
    "main_category": "신발",
    "sub_category": "패딩/퍼 신발",
    "image": "http://example.com/image/padding1.jpg",
    "description": "겨울철 필수 아이템, 보온성 뛰어난 다운 부츠.",
    "brand": "노스페이스"
  },
  {
    "name": "컬럼비아 방한 부츠",
    "price": 97000,
    "url": "http://example.com/product/padding2",
    "main_category": "신발",
    "sub_category": "패딩/퍼 신발",
    "image": "http://example.com/image/padding2.jpg",
    "description": "눈길에도 미끄러지지 않는 퍼 안감 방한 부츠.",
    "brand": "컬럼비아"
  },
  {
    "name": "아이더 여성 겨울부츠",
    "price": 99000,
    "url": "http://example.com/product/padding3",
    "main_category": "신발",
    "sub_category": "패딩/퍼 신발",
    "image": "http://example.com/image/padding3.jpg",
    "description": "퍼 안감과 발목을 감싸주는 따뜻한 디자인.",
    "brand": "아이더"
  },
  {
    "name": "팀버랜드 클래식 워커",
    "price": 198000,
    "url": "http://example.com/product/boots1",
    "main_category": "신발",
    "sub_category": "부츠/워커",
    "image": "http://example.com/image/boots1.jpg",
    "description": "방수 기능과 튼튼한 내구성을 갖춘 팀버랜드 워커.",
    "brand": "팀버랜드"
  },
  {
    "name": "닥터마틴 1460",
    "price": 189000,
    "url": "http://example.com/product/boots2",
    "main_category": "신발",
    "sub_category": "부츠/워커",
    "image": "http://example.com/image/boots2.jpg",
    "description": "시그니처 옐로우 스티치와 견고한 가죽 부츠.",
    "brand": "닥터마틴"
  },
  {
    "name": "레드윙 아이언레인저",
    "price": 319000,
    "url": "http://example.com/product/boots3",
    "main_category": "신발",
    "sub_category": "부츠/워커",
    "image": "http://example.com/image/boots3.jpg",
    "description": "헤리티지 스타일과 뛰어난 내구성의 프리미엄 워커.",
    "brand": "레드윙"
  },
  {
    "name": "락포트 옥스포드 구두",
    "price": 135000,
    "url": "http://example.com/product/dress1",
    "main_category": "신발",
    "sub_category": "구두",
    "image": "http://example.com/image/dress1.jpg",
    "description": "편안함과 격식을 갖춘 정장용 구두.",
    "brand": "락포트"
  },
  {
    "name": "닥스 정장 구두",
    "price": 178000,
    "url": "http://example.com/product/dress2",
    "main_category": "신발",
    "sub_category": "구두",
    "image": "http://example.com/image/dress2.jpg",
    "description": "고급스러운 가죽과 세련된 실루엣.",
    "brand": "닥스"
  },
  {
    "name": "질스튜어트 남성 로퍼",
    "price": 158000,
    "url": "http://example.com/product/dress3",
    "main_category": "신발",
    "sub_category": "구두",
    "image": "http://example.com/image/dress3.jpg",
    "description": "캐주얼 정장 모두에 어울리는 슬립온 스타일.",
    "brand": "질스튜어트"
  },
  {
    "name": "버켄스탁 아리조나",
    "price": 85000,
    "url": "http://example.com/product/sandal1",
    "main_category": "신발",
    "sub_category": "샌들/슬리퍼",
    "image": "http://example.com/image/sandal1.jpg",
    "description": "편안한 아치 서포트를 제공하는 캐주얼 샌들.",
    "brand": "버켄스탁"
  },
  {
    "name": "나이키 베나시 슬리퍼",
    "price": 39000,
    "url": "http://example.com/product/sandal2",
    "main_category": "신발",
    "sub_category": "샌들/슬리퍼",
    "image": "http://example.com/image/sandal2.jpg",
    "description": "간편하게 신을 수 있는 데일리 슬리퍼.",
    "brand": "나이키"
  },
  {
    "name": "아디다스 아딜렛",
    "price": 42000,
    "url": "http://example.com/product/sandal3",
    "main_category": "신발",
    "sub_category": "샌들/슬리퍼",
    "image": "http://example.com/image/sandal3.jpg",
    "description": "미끄럼 방지와 쿠셔닝이 뛰어난 EVA 슬리퍼.",
    "brand": "아디다스"
  }
        ]

        for product in products:
            res = requests.post(es_url, json=product)
            print(res.json())

if __name__ == "__main__":
        init_elasticsearch_data()