<p align="center">
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcRZyWw%2FbtrJ2nbV0Ly%2FV0thL6tNjJKnkPrHsiYlJK%2Fimg.png">
</p>

# 📖[웹소설] 일타강사 AI의 기막힌 추천 (웹타추)
크롤링한 웹소설들의 줄거리를 자연어 처리를 하고 벡터 임베딩하여

사용자가 좋아요를 누른 소설의 줄거리와 유사도가 높은 작품을 추천해주는 웹사이트

# 📕INTRO
* 자연어 처리와 벡터 임베딩을 통한 줄거리 유사도 비교로 웹소설을 추천
* 메인 페이지에서 [네이버 시리즈 소설 일간 순위](https://series.naver.com/novel/top100List.series) 크롤링 해서 20위까지 보여줌
* 각 작품에 사용자들이 작성한 리뷰 키워드 표시와 좋아요를 누른 소설의 줄거리 키워드 표시
* **개발 기간**: 2022.06.02 ~ 2022.06.13
* **개발 인원(4명)**: 김동근, 노을, 이정아, 이현경
* **Team Repository** [![github_icon](https://img.shields.io/badge/Github-000000?style=flat-square&logo=github&logoColor=white)](https://github.com/cmjcum/webtachu)
* **S.A** [블로그로 이동(☞ﾟヮﾟ)☞](https://cold-charcoal.tistory.com/85)

# 📗PROJECT
### 사용 기술
* Python 3.8
* Django 3.2
* Crawling(bs4 4.11, selenium 4.2)
* NLP(KoNLPy 0.6)
* Vector Embedding(gensim 3.8 - Doc2Vec)

### 핵심 기능
웹소설의 줄거리를 자연어 처리와 벡터 임베딩을 이용해 분석하고 추천
* 선호작을 누른 작품들의 스토리와 유사도가 높은 작품들을 추천, 선호작을 아직 누르지 않았다면 별점이 높은 작품들을 추천
* Today best top 20 - 네이버 시리즈의 일간 Top100에서 20위까지 크롤링해서 보여주기
* 회원가입 및 로그인 - 장고 내장 모델 사용
* 장르별 페이지에서 작품들을 Django 내장 Paginator를 사용하여 한 페이지 당 10 개씩 표시
* 작품 상세 페이지에서 리뷰들의 키워드를 분석해서 가장 많은 키워드 상위 5개, 마이 페이지에서 선호작 누른 작품들의 줄거리 키워드 빈도수 상위 10개 표시
* 리뷰 CRUD

### 맡은 부분
<details>
<summary>웹소설 작품 정보 크롤링 <a href="https://colab.research.google.com/drive/1e--L4ZwZQann99Y9ZwBTG-7VlB9PW4DM?usp=sharing">📑코드(코랩)</a></summary>

네이버 시리즈에서 판타지 장르와 로맨스 판타지 장르를 크롤링 했습니다.<br>
BeautifulSoup과 Selenium을 함께 사용했습니다.<br>
bs로 전체 작품 목록에서 각 작품들의 상세 페이지로 연결되는 url을 크롤링 하고 크롤링한 url에 각각 접속하여 작품들의 상세 정보를 크롤링 하는데 이때 네이버 시리즈에서 작품의 전체 줄거리는 각 작품의 페이지에서 더보기 버튼을 눌러야 보이기 때문에 selenium을 사용했습니다.
</details>
<details>
<summary>추천 모델 제작 <a href="https://colab.research.google.com/drive/1MyePVoA6OAbsVkR2ErudTtkmpwIPoHno?usp=sharing">📑코드(코랩)</a></summary></summary>

KoNLPy의 Mecab을 이용하여 각 소설의 줄거리를 형태소 단위로 토큰화 하고 gensim의 Doc2Vec으로 벡터화 해서 코사인 유사도를 비교하는 모델을 만들었습니다.
</details>
<details>
<summary>작품 추천 <a href="https://github.com/zeonga1102/webtachu/blob/master/books/views.py#L47">📑코드</a></summary></summary>

제작한 모델을 이용해서 사용자가 좋아요를 누른 작품의 줄거리와 코사인 유사도가 높은 작품을 추천합니다.<br>
좋아요를 누른 작품들의 키워드 중 빈도수가 높은 20개와 가중치를 준 제목 키워드 3개에 대해 벡터화를 하고 제작한 모델에서 유사도가 높은 작품 5개를 선정합니다.<br>
만약 좋아요를 누른 작품이 없다면 별점이 높은 작품 5개를 추천합니다.
</details>
<details>
<summary>작품 리뷰 및 좋아요 누른 작품 키워드 표시 <a href="https://github.com/zeonga1102/webtachu/blob/master/books/book_views.py#L102">📑코드</a></summary></summary>

형태소 분석을 통해 전체 리뷰와 좋아요를 누른 소설들의 줄거리에서 빈도수가 높은 키워드들을 뽑아냈습니다<br>
함수로 만들어서 사용했습니다.<br>
함수 사용 예시입니다. 각 소설에서 리뷰 키워드를 뽑아내는 부분입니다. <a href="https://github.com/zeonga1102/webtachu/blob/master/books/book_views.py#L88">📑코드</a>
</details>
<details>
<summary>작품 상세 정보 및 리뷰 조회 <a href="https://github.com/zeonga1102/webtachu/blob/master/books/book_views.py#L80">📑코드</a></summary></summary>

작품별 페이지에서 각 작품의 상세 정보와 그 작품에 달린 리뷰들을 조회합니다.<br>
사용자가 해당 작품에 좋아요를 눌렀는지와 리뷰 키워드를 함께 프론트로 보냅니다.
</details>

### ERD
![image](https://user-images.githubusercontent.com/104331869/185334447-e9eaabb2-c3e0-4d1a-95de-5bb09921b73a.png)

# 🛠Troubleshooting

# 🖋회고

# 📘Credit
* 웹소설 작품 정보 - [네이버 시리즈](https://series.naver.com/novel)
