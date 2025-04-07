# Fiction2Toon
![thumbnail](docs/thumbnail.jpg)

## 📝 목차
- [📌 프로젝트 소개](#-프로젝트-소개)
- [🗝️ 주요 기능](#️-주요-기능)
- [⚙️ 시스템 구조](#️-시스템-구조)
- [🛠️ 기술 스택](#️-기술-스택)
- [👪 팀원 소개](#-팀원-소개)

## 📌 프로젝트 소개
### [>> Fiction2Toon이 궁금하다면? <<](https://drive.google.com/file/d/1M8VBlzS4hvBmMw2TYjo36vvuPfxctN-H/view?usp=sharing)

**Fiction2Toon**은 여러분의 소설을 쉽고 빠르게 웹툰으로 변신시켜주는 원클릭 AI 서비스입니다.

- 개발 기간: 2024.12.30 ~ 2025.02.13
- 현재 상태: **서비스 중단💤**

## 🗝️ 주요 기능
### 1. 회원제 운영
![login](docs/webpage_login.png)
- 회원가입 및 로그인 기능
- 회사 단위 계정 운영
- Spring Security를 통한 인증 및 권한 관리

### 2. 게시판
![board](docs/webpage_mainboard.png)
- 공지사항, Q&A, 후기 게시판으로 구성
- 게시글 작성, 수정, 삭제 기능
- 댓글 작성, 수정, 삭제 기능
- 게시글 분류 및 제목, 작성자 기반 검색 기능

### 3. 웹툰 생성 서비스
![webtoon](docs/webpage_loading.png)
- .pdf 또는 .txt 파일만 업로드 허용
- 업로드된 파일은 AI 모델이 탑재된 fastAPI 서버로 전송
- AI 모델은 업로드된 파일을 적절한 청크로 나누어 이미지컷 생성

### 4. 모델 히스토리
![history](docs/webpage_history.png)
- 사용자가 생성한 웹툰의 모델 히스토리 저장
- 개별 히스토리는 공개 설정 시 모두가 볼 수 있으며, 비공개로 설정할 경우 본인 소속 회사의 인원만 열람 가능

## ⚙️ 시스템 구조
![architect](docs/architect.png)

## 🛠️ 기술 스택
### Web
![Java](https://img.shields.io/badge/Java-007396?style=flat-square&logo=java&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white)
![Spring Security](https://img.shields.io/badge/Spring%20Security-6DB33F?style=flat-square&logo=springsecurity&logoColor=white)
![JPA](https://img.shields.io/badge/JPA-6DB33F?style=flat-square&logo=springdatajpa&logoColor=white)
![Gradle](https://img.shields.io/badge/Gradle-02303A?style=flat-square&logo=gradle&logoColor=white)
![Thymeleaf](https://img.shields.io/badge/Thymeleaf-005E7C?style=flat-square&logo=thymeleaf&logoColor=white)
![jQuery](https://img.shields.io/badge/jQuery-0769AD?style=flat-square&logo=jquery&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=flat-square&logo=bootstrap&logoColor=white)
![MSSQL](https://img.shields.io/badge/MSSQL-CC2927?style=flat-square&logo=microsoftsqlserver&logoColor=white)

### Cloud
![Azure](https://img.shields.io/badge/Azure-0089D6?style=flat-square&logo=microsoftazure&logoColor=white)
![Azure Web App](https://img.shields.io/badge/Azure%20Web%20App-0089D6?style=flat-square&logo=microsoftazure&logoColor=white)
![Azure SQL Database](https://img.shields.io/badge/Azure%20SQL%20Database-0089D6?style=flat-square&logo=microsoftazure&logoColor=white)
![Azure Blob Storage](https://img.shields.io/badge/Azure%20Blob%20Storage-0089D6?style=flat-square&logo=microsoftazure&logoColor=white)

### AI/Data
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?style=flat-square&logo=googlecolab&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FD7A00?style=flat-square&logo=huggingface&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-00A3FF?style=flat-square&logo=openai&logoColor=white)
![KoBART](https://img.shields.io/badge/kobart-FF6F20?style=flat-square&logo=ko-fi&logoColor=white)
![Stable Diffusion](https://img.shields.io/badge/Stable%20Diffusion-000000?style=flat-square&logo=stable-diffusion&logoColor=white)
![UNet](https://img.shields.io/badge/UNet-FF6F20?style=flat-square&logo=ko-fi&logoColor=white)
![IP-Adapter](https://img.shields.io/badge/IP%20Adapter-FF6F20?style=flat-square&logo=ko-fi&logoColor=white)

### Collaboration
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-000000?style=flat-square&logo=notion&logoColor=white)
![MS Teams](https://img.shields.io/badge/MS%20Teams-6264A7?style=flat-square&logo=microsoftteams&logoColor=white)
![Figma](https://img.shields.io/badge/Figma-F24E1E?style=flat-square&logo=figma&logoColor=white)

## 👪 팀원 소개
| Web | Web |
| :---: | :---: |
|[<img src="https://github.com/gaeul-3041.png" width="100px">](https://github.com/gaeul-3041)|[<img src="https://github.com/seonghoonL.png" width="100px">](https://github.com/seonghoonL)|
|[진현](https://github.com/gaeul-3041)|[이성훈](https://github.com/seonghoonL)|

| AI(NLP) | AI(NLP) |
| :---: | :---: |
|[<img src="https://github.com/leesanghaw.png" width="100px">](https://github.com/leesanghaw)|[<img src="https://github.com/tae2on.png" width="100px">](https://github.com/tae2on)|
|[이상화](https://github.com/leesanghaw)|[황태언](https://github.com/tae2on)|

| AI(Image) | AI(Image) |
| :---: | :---: |
|[<img src="https://github.com/Lee-hyeonje.png" width="100px">](https://github.com/Lee-hyeonje)|[<img src="https://github.com/MangV2.png" width="100px">](https://github.com/MangV2)|
|[이현제](https://github.com/Lee-hyeonje)|[정민규](https://github.com/MangV2)|
