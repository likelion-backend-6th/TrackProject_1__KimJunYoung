# TrackProject_1__KimJunYoung


## SNS 백엔드 서비스 개발 프로젝트

---

<br>

### 0. 환경 및 버전

<br>

언어
- Python: 3.11.3

<br>

라이브러리
- Django: 4.2.4
- djangorestframework: 3.14.0
- drf-spectacular: 0.26.4
- psycopg2-binary: 2.9.7
- gunicorn: 21.2.0

<br>

클라우드
- backend-server: ubuntu 20.04
- db-server: ubuntu 20.04

<br>

도커
- Docker: 24.0.5
- backend-image: python-3.11-alpine
- db-image: postgresql-13

<br>

### 1. 백엔드 DB 설계

- [x] Post

|Field|Type|Constraint|
|------|---|---|
|title|CHAR(max_length=100)|NOT_NULL|
|body|TEXT|NOT_NULL|
|owner|INTEGER|FOREIGN KEY User, NOT NULL|
|created_at|DATETIME|auto_now_add|
|updated_at|DATETIME|auto_now|


- [x] follow

|Field|Type|Constraint|
|------|---|---|
|follower|INTEGER|FOREIGN KEY User, NOT NULL|
|following|INTEGER|FOREIGN KEY User, NOT NULL|
|created_at|DATETIME|auto_now_add|

<br>

### 2. 백엔드 API 개발


- 유저
    - [x] 사용자 본인을 제외한 전체 사용자 목록을 확인할 수 있다.
    > method: GET <br>
    > API: [/users/](http://lion-lb-prod-19483051-7661c2c0d955.kr.lb.naverncp.com/users/)

- 게시글
    - 사용자는 게시글을 올릴 수 있다.
    > method: POST <br>
    > [/blog/post/](http://lion-lb-prod-19483051-7661c2c0d955.kr.lb.naverncp.com/blog/post/)

    - 사용자는 본인의 게시물을 모아볼 수 있다.
    > method: GET <br>
    > [/blog/post/my-post/](http://lion-lb-prod-19483051-7661c2c0d955.kr.lb.naverncp.com/blog/post/my-post/)

    - 사용자는 본인의 게시물을 수정하거나, 삭제할 수 있다.
    > method: PUT <br>
    > [/blog/post/{id:int}](http://lion-lb-prod-19483051-7661c2c0d955.kr.lb.naverncp.com/blog/post/10)

    > method: DELETE <br>
    > [/blog/post/{id:int}](http://lion-lb-prod-19483051-7661c2c0d955.kr.lb.naverncp.com/blog/post/10)

- follow
    - 사용자는 다른 사용자를 follow(unfollow)할 수 있다.
    > method: POST <br>
    > [/follow/](http://lion-lb-prod-19483051-7661c2c0d955.kr.lb.naverncp.com/follow/)

    > method: POST <br>
    > [/follow/unfollow/{username}/](http://lion-lb-prod-19483051-7661c2c0d955.kr.lb.naverncp.com/follow/unfollow/test1)


    - 사용자는 follow한 사람들 목록을 확인할 수 있다.
    > method: GET <br>
    > [/follow/follower/](http://lion-lb-prod-19483051-7661c2c0d955.kr.lb.naverncp.com/follow/follower)

    - 사용자는 나를 follow하고 있는 사람들 목록을 확인할 수 있다.
    > method: GET <br>
    > [/follow/following/](http://lion-lb-prod-19483051-7661c2c0d955.kr.lb.naverncp.com/follow/following)

    - 사용자는 follow한 사람들이 올린 게시물을 모아볼 수 있다.
    > method: GET <br>
    > [/blog/post/following-post/](http://lion-lb-prod-19483051-7661c2c0d955.kr.lb.naverncp.com/follow/follower)

<br>

### 3. 더미데이터 추가

- [x] 사용자 5명 이상
- [x] 사용자당 게시글 3개 이상

<br>

### 4. 테스트 코드 작성


- [x] 전체 사용자 목록에서 자신을 제외한 목록이 잘 나오는지 테스트
- [x] 본인의 게시물만 수정, 삭제가 가능한지 테스트
- [x] follow / unfollow 기능이 잘 작동하는지 테스트
- [x] follow한 사람들이 올린 게시물을 잘 확인할 수 있는지 테스트


### 5. 배포

- [x] runserver, gunicorn 등을 사용해서 배포
- [x] 어디서든 API호출이 가능하도록 백엔드 서버를 클라우드 서비스를 통해 배포

### 6. CICD Pipeline 작성

- [x] Github actions로 구현
- [x] push가 됐을때, 테스트코드를 실행하여, 테스트가 정상 작동하는지 확인하고, 정상 작동하면, 서버에 새 버전을 배포


<br><br>

## 도전 미션 개요

---

### 백엔드 서버 분리

- [x] 백엔드 서버와 DB 서버를 물리적으로 분리
- NCloud 인스턴스로 백엔드서버와 DB서버를 각각 생성하였습니다.

### 도커 컨테이너로 배포

- [x] docker image를 이용한 container로 배포
- NCP Container Registry에 빌드한 docker 이미지를 올려두고 각 인스턴스에서 받아와 컨테이너로 실행하였습니다.

### 로드밸런서를 통해 배포

- [x] 인스턴스에 직접 접근하는 대신 로드밸런서를 통해 API를 호출할 수 있도록 배포
- NCP LoadBalancer를 생성하여 배포하였습니다.

### API문서 작성

- [x] 프론트엔드 개발자가 API를 확인할 수 있도록 웹에서 접근 가능한 API문서 작성
- [API docs](http://lion-lb-prod-19483051-7661c2c0d955.kr.lb.naverncp.com/api/docs/#/)

### CICD Pipeline 작성

- [x] PR이 있을때, 테스트코드를 실행하여, 테스트가 정상 작동하는지 확인
- CI.yaml 에서 PR이 있을때 lint 체크와 테스트코드 실행을 하고 정상완료되었을때 NCP Container Registry에 push하고 CI가 정상완료 되었을때 CD.yaml이 동작하여 백엔드 인스턴스에 접속하여 업로드한 이미지를 pull받아와 컨테이너를 실행시켜 배포합니다.