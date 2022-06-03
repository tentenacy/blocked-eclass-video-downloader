# 이클래스 막힌 동영상 다운로더

## 기능

- 일반적인 다운로드(오른쪽 클릭 > 다른 이름으로 저장)가 막힌 동영상 다운로드
- 기한이 지난 강의 다운로드
- 하나의 강의에 분리된 동영상을 비교적 편리하게 다운로드
- 파일을 다운로드하기 위해 적용된 솔루션: 3개

## 입력

- 파일 이름(필수)
    - 지정 위치에 저장될 파일의 이름입니다.
- 저장 위치(필수)
    - 다운로드할 파일의 저장 위치입니다.
- lecture_weeks(필수)
    - 강의 순번입니다. 현재 수강하는 과목 중에서 강의 순번이 중복되거나 할 수 없습니다.
    - **예를 들어, 1주차 강의가 4개이고, 2주차 강의가 4개, ..., 이런 식이면 1주차 강의에서 첫 번째 동영상의 lecture_weeks는 1이고, 2주차 강의에서 두 번째 동영상의 lecture_weeks는 6입니다.**

![Untitled](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/99e43723-56bf-43f9-8e51-69ea5bd26b77/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220603%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220603T151445Z&X-Amz-Expires=86400&X-Amz-Signature=1481206a2c5f72791f71d5d96c622ef0abc65225d0208e77aa2e8313b6dcf97d&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22&x-id=GetObject)

- item_id(선택)
    - 하나의 강의에 여러 강의(Table of contents)가 있는 경우 강의를 구분하는 데 사용되는 식별자입니다.
    - 위 경우가 아니라면 **기본적으로 item_id는 필요로 하지 않습니다.**
- JSESSIONID(필수)
    - 사용자의 로그인 세션을 유지하기 위한 식별자입니다.
    - 로그인 세션이 살아있는 동안에는 변경되지 않기 때문에, 한 번 입력해놓으면 일일이 JSESSIONID를 확인할 필요가 없습니다.

## 사용법

0. exe 파일 실행 시 같은 폴더에 ui 파일이 위치해야 함

1. 다운로드할 과목의 이클래스 페이지로 진입

![Untitled](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/43bb921c-a4b6-4d6f-8ad2-3940a2ec54e2/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220603%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220603T152001Z&X-Amz-Expires=86400&X-Amz-Signature=715ea94c3fe79f957b81b7e01c1e9dd8831d5f3115f0af5ce34a794bf1b24f71&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22&x-id=GetObject)

2. 개발자 도구(F12 or ctrl+shift+I or 직접(크롬 도구 더보기 > 개발자 도구)) > Application(안 보이면 우측 '>>' 클릭) > Storage > Cookies 하위 항목 선택 후 JSESSIONID 확인

    - JSESSIONID는 한 번 설정해놓으면 로그아웃되지 않는 한, 바꿀 필요 없음

![Untitled](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/904ef682-bd1f-4c98-9d3c-3a51bc667b89/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220528%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220528T193148Z&X-Amz-Expires=86400&X-Amz-Signature=2568a34f991ced8c2e6d10f1b2d78353eb3ca86d4d3ea44e476299fe33fc889d&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22&x-id=GetObject)

2-1(선택). 개발자 도구 > Network > Filter > online_view_navi.acl 입력 후 Payload에서 item_id 확인

   (Network 화면이 안 보일 시 ctrl+R)

   ![Untitled](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/a369b343-eef3-4351-a07b-b643227c37e6/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220603%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220603T152641Z&X-Amz-Expires=86400&X-Amz-Signature=1d5a67ad9f224d8bc8434cecaebb2986c66211e7074f910bce9e2a451d8f3435&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22&x-id=GetObject)


4. 프로그램에 파일 이름, 저장 위치, lecture_weeks, item_id(선택), JSESSIONID를 입력하고 다운로드

## 유의사항

- 한국공학대학교 이클래스에 한해서만 사용 가능
- 일부 동영상은 다운로드 되지 않거나 오디오 파일만 다운로드 되는 경우가 존재함
- 분리된 동영상을 하나의 영상으로 병합하지는 않음

  이 때에는, 파일명 끝에 순번이 있기 때문에 인기 동영상 플레이어로 시청하기를 권함
