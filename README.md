# 이클래스 막힌 동영상 다운로더

## 기능

- 일반적인 다운로드가 막힌 동영상 다운로드
- 하나의 강의에 분리된 동영상을 비교적 편리하게 다운로드

## 입력

- 파일 이름
    - 지정 위치에 저장될 파일의 이름입니다.
- 저장 위치
    - 다운로드할 파일의 저장 위치입니다.
- lecture_weeks
    - 강의 순번입니다. 현재 수강하는 과목 중에서 강의 순번이 중복되거나 할 수 없습니다.
    - `N주차 강의` 이런 거 아닙니다.
- item_id
    - 하나의 강의에 여러 강의(Table of contents)가 있는 경우 이를 구분하는 식별자입니다.
    - 이 경우 강의는 같기 때문에, 강의 순번(lecture_weeks)은 같습니다.
- JSESSIONID
    - 사용자의 로그인 세션을 유지하기 위한 식별자입니다.
    - 로그인 세션이 살아있는 동안에는 변경되지 않습니다.

## 사용법

1. 개발자 도구(F12 or ctrl+shift+I or 직접) > Storage > Cookies 하위 항목 선택 후 JSESSIONID 확인

![Untitled](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/904ef682-bd1f-4c98-9d3c-3a51bc667b89/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220528%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220528T191626Z&X-Amz-Expires=86400&X-Amz-Signature=c9ea4228fc65f4202e6e76ac920e5d3f53c5e7a784d0069ca1e77c6e2ab42961&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22&x-id=GetObject)

2. 개발자 도구(F12 or ctrl+shift+I or 직접) > Network > Filter > online_view_navi.acl 입력 후 Response에서 lecture_weeks,  item_id 확인

   (Network 화면이 안 보일 시 ctrl+R)

    - Response에서 path로 넘어가면 동영상 강의를 다운로드할 수 있지만 일부 강의에서는 다운로드가 막혀 있기 때문에 수동으로 하는 거보다는 프로그램을 사용하기를 권장

   ![Untitled](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/a95d9b9b-ea49-4014-af14-c2fc0624d055/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220528%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220528T191516Z&X-Amz-Expires=86400&X-Amz-Signature=bf387a5d6db4b846cc9ac2d8ab2ad438042312575465b37451f894c367e26333&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22&x-id=GetObject)


3. 프로그램에 파일 이름, 저장 위치, lecture_weeks, item_id, JSESSIONID를 입력하고 다운로드

![Untitled](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/02588ae2-4e5d-40c7-8423-884a640868ff/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220528%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220528T191638Z&X-Amz-Expires=86400&X-Amz-Signature=759148ee23bed25477268020c0241446e5c6d50e60d67791d35c80d91fb5b197&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22&x-id=GetObject)

## 유의사항

- 현재 2개의 솔루션만 적용되어 있어서 일부 동영상은 다운로드 되지 않거나 오디오 파일만 다운로드 되는 경우가 존재함
    - 강의 업로드 서버마다 다 다른 방식의 보안이 적용되어 있어서 일반적인 다운로드는 사실상 힘듦
    - 강의 업로드 서버는 교수별로 다른 걸로 확인됨
- 분리된 동영상을 하나의 영상으로 병합하지는 않음

  이 때에는, 파일명 끝에 순번이 있기 때문에 인기 동영상 플레이어로 시청하기를 권함