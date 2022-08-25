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
<summary>추천 모델 제작 <a href="https://colab.research.google.com/drive/1MyePVoA6OAbsVkR2ErudTtkmpwIPoHno?usp=sharing">📑코드(코랩)</a></summary>

KoNLPy의 Mecab을 이용하여 각 소설의 줄거리를 형태소 단위로 토큰화 하고 gensim의 Doc2Vec으로 벡터화 해서 코사인 유사도를 비교하는 모델을 만들었습니다.
</details>
<details>
<summary>작품 추천 <a href="https://github.com/zeonga1102/webtachu/blob/master/books/views.py#L47">📑코드</a></summary>

제작한 모델을 이용해서 사용자가 좋아요를 누른 작품의 줄거리와 코사인 유사도가 높은 작품을 추천합니다.<br>
좋아요를 누른 작품들의 키워드 중 빈도수가 높은 20개와 가중치를 준 제목 키워드 3개에 대해 벡터화를 하고 제작한 모델에서 유사도가 높은 작품 5개를 선정합니다. 이때 이미 좋아요를 누른 작품은 추천에서 제외합니다.<br>
만약 좋아요를 누른 작품이 없다면 별점이 높은 작품 5개를 추천합니다.
</details>
<details>
<summary>작품 리뷰 및 좋아요 누른 작품 키워드 표시 <a href="https://github.com/zeonga1102/webtachu/blob/master/books/book_views.py#L102">📑코드</a></summary>

형태소 분석을 통해 전체 리뷰와 좋아요를 누른 소설들의 줄거리에서 빈도수가 높은 키워드들을 뽑아냈습니다<br>
함수로 만들어서 사용했습니다.<br>
함수 사용 예시입니다. 각 소설에서 리뷰 키워드를 뽑아내는 부분입니다. <a href="https://github.com/zeonga1102/webtachu/blob/master/books/book_views.py#L88">📑코드</a>
</details>
<details>
<summary>작품 상세 정보 및 리뷰 조회 <a href="https://github.com/zeonga1102/webtachu/blob/master/books/book_views.py#L80">📑코드</a></summary>

작품별 페이지에서 각 작품의 상세 정보와 그 작품에 달린 리뷰들을 조회합니다.<br>
사용자가 해당 작품에 좋아요를 눌렀는지와 리뷰 키워드를 함께 프론트로 보냅니다.
</details>
<details>
<summary>좋아요 추가 및 삭제 <a href="https://github.com/zeonga1102/webtachu/blob/master/books/book_views.py#L126">📑코드</a></summary>

해당 작품에 좋아요를 눌렀을 때 현재 사용자가 이미 좋아요를 누른 상태인지 아닌지 판별하여 만약 좋아요를 누른 상태였다면 해당 작품을 favorite에서 삭제하고 누르지 않은 상태였다면 추가합니다.
</details>
<details>
<summary>작품 검색 <a href="https://github.com/zeonga1102/webtachu/blob/master/books/views.py#L65">📑코드</a></summary>

제목을 기준으로 작품을 검색합니다.<br>
사용자가 입력한 검색어를 제목에 포함하고 있으면 결과로 보여줍니다.
</details> 

### ERD
![image](https://user-images.githubusercontent.com/104331869/185334447-e9eaabb2-c3e0-4d1a-95de-5bb09921b73a.png)

# 🛠Troubleshooting
### 최근 좋아요 누른 작품 최신순 정렬
모델을 만들 때 좋아요는 UserModel 아래에 ManyToManyField로 BookModel을 참조하도록 만들었습니다. 저장과 조회, 추천 작품 선정은 무리 없이 되지만 정렬이 문제였습니다. 좋아요를 누른 순서대로 정렬이 됐으면 해서 처음에는 orderby를 이용해서 id로 정렬을 했는데 중간 테이블인 user_favorite의 id로 정렬이 되는게 아니라 BookModel의 id로 정렬이 되어 최신순 정렬이 되지 않아 슬라이싱을 이용해서 역순으로 바꿔보기도 했습니다. 하지만 그래도 원하는대로 정렬이 되지 않았습니다. 그래서 raw query를 이용해 중간 테이블에 접근하여 해결했습니다.<br>
[📑코드](https://github.com/zeonga1102/webtachu/blob/master/users/views.py#L118)

# 🖋회고
장고를 이용한 첫 프로젝트였는데 프레임워크 사용에 큰 어려움을 느끼진 않았던 것 같다. 오히려 ORM을 사용할 수 있어서 CRUD 같은 부분은 플라스크보다 편한 것 같다.<br>
추천 방식에는 여러가지가 있지만 웹소설에 대한 사용자들의 평점 데이터를 구할 수가 없어서 자연어 처리와 벡터 임베딩을 이용한 것인데 데이터가 있었다면 협업 필터링도 써볼 수 있었을 것 같다. 협업 필터링을 못 써본게 아쉽기는 하다. 아무래도 줄거리로 추천을 하기엔 줄거리는 정말 소설의 단편만을 담고 있기 때문에 추천 작품에 대한 사용자들의 만족도가 높지 않을 것 같다. 그래도 제작한 모델이 추천해주는 작품들이 제목이나 줄거리만 보면 비슷한 결인 것 같아서 성능 자체는 괜찮은 것 같다.<br>
이번 프로젝트 후반에는 팀원들과 다함께 화면을 보며 디자인 변경이나 기능 추가, 버그 픽스 등을 즉각적으로 나눠서 했는데 작업 속도도 빠른 것 같고 의견 조율도 빨리 되어서 좋은 방식이었던 것 같다.<br>
우리 팀원들 모두가 웹소설을 좋아해서 이번에 웹소설을 주제로 프로젝트를 진행한 것이었는데 좋아하는 분야이다보니 이전보다 더 재밌게 작업할 수 있었다.<br>
**[팀 회고 보러가기(☞ﾟヮﾟ)☞](https://cold-charcoal.tistory.com/95)**
# 📘Credit
* 웹소설 작품 정보 - [네이버 시리즈](https://series.naver.com/novel)
