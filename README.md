# place_recommender
협업 필터링 기반 국내 여행지 추천 시스템 프로제트

---

## 프로젝트 개요
코로나19 이후 현대인들의 삶은 여가, 생활, 근무 환경, 교육 방식 등 다방면에서 변화를 맞이했다. 특히 장기간 시행된 사회적 거리두기와 사적모임 축소는 개인화 및 소규모 형태의 여행 행태를 증가시켰다. 이러한 양상은 거리두기 해제 이후에도 꾸준히 늘고 있고, 실제로 한국관광공사의 통계에 따르면 최근 3년간 '당일치기(15%)', '한달살기(15%)', '즉흥여행(20.3%)' 등의 검색량이 증가하였다. 해당 자료로 미루어 보아 개별화 및 다양화된 여행에 대한 수요가 증가하고 있으며, 이에 개인의 취향을 반영할 수 있는 여행지 추천 서비스의 필요성을 취지로 해당 웹 어플리케이션을 기획하게 되었다.

본 프로젝트의 목적은 여행 정보 시스템의 추천 알고리즘을 적용하여 사용자들의 취향이 반영된 여행지를 선별해주는 것이다. 기존의 여행지 추천 시스템이 적용된 서비스에서는 여행 지역 및 방문 목적에 따른 유명 관광지를 추천해주고 있으나, 개개인의 취향을 반영하지는 않는 것으로 확인되었다. 본 어플리케이션을 활용한다면 사용자들은 여행 계획에 소요되는 시간을 절약할 수 있고, 개인의 취향을 반영하도록 추천 여행지를 분산시키킴으로써 기존에 각광받지 못했던 명소들의 관광 산업 및 해당 지역의 상권 또한 발전할 것으로 기대하고 있다.

## 아키텍쳐 및 구성 요소
### 시스템 아키텍처
  
![image](https://user-images.githubusercontent.com/56084058/230799209-f37d6785-bad8-4d1e-99f8-a56a2690f156.png)


### 개발 구성
**Web Page**
: ReactJS를 활용하여 웹 페이지 랜더링, 카카오맵 API로 지도 기능 구성

**Server**
: 회원가입 및 로그인, 여행지 검색, 리뷰 입력 등의 기능은 Node Express 기반의 API를 구현하여 처리. 추천 시스템에 필요한 Matrix Factorization 및 Utility Matrix 생성 처리는 Flask 서버에서 수행한 후 Express 서버와 API 통신. 각 서버는 MySQL DB에 동시에 접근하여 데이터 처리가 가능하도록 구현

**Recommender System**
: Data Preprocessing 및 분석을 위해 Google Colab 활용. 여행지 추천에 MF 기반 알고리즘 적용

**데이터 수집**
: Selenium과 Beautiful Soup을 활용하여 Google Map의 각 여행지별 정보(리뷰 평균 평점, 리뷰 수, 장소 유형, 위도/경도, 키워드, 소개 글)과 리뷰 데이터(여행지, 유저ID, 별점)을 수집

## Matrix Factorization

![image](https://user-images.githubusercontent.com/56084058/230799495-e6e498b7-1cc8-40e8-81d0-e9034c38d005.png)

User-Item의 Rating으로 구성된 Utility Matrix를 User-Latent와 Item-Latent 행렬로 분해하는 기법이다. 본 프로젝트에서는 분해된 각 행렬을 ML 방식으로 학습하여 최적화하도록 구현했다. 추가적으로 도메인, 사용자, 여행지에 대한 Bias를 Baseline Predictor를 적용하여 추천 시스템의 성능을 개선했다.

## 실행 화면

![image](https://user-images.githubusercontent.com/56084058/230799539-496dabbf-da34-47e6-bd1f-1d51588d7c68.png)

![image](https://user-images.githubusercontent.com/56084058/230799565-d74d100e-a422-4cc9-a30b-9380da6ee3a5.png)

## Ajou Softcon
https://softcon.ajou.ac.kr/works/works.asp?uid=691&category=A
