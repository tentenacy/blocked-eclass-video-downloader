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
    - 강의 순번입니다.
    - **예를 들어, 1주차(아래 사진에서는 2주차) 강의가 4개이고, 2주차(아래 사진에서는 3주차) 강의가 4개, ..., 이런 식이면 1주차 강의에서 첫 번째 동영상의 lecture_weeks는 1이고, 2주차 강의에서 두 번째 동영상의 lecture_weeks는 6입니다.**
    - (참고) 같은 주차에서 lecture_weeks가 오름차순으로 정렬되어 있지 않은 경우도 있습니다. 예를 들어, 2주차 강의의 1, 2번째 동영상의 lecture_weeks가 각각 5, 6이 아니고, 6, 5인 경우도 있습니다.

![Untitled 1](https://user-images.githubusercontent.com/76826021/172287873-37aaac86-088e-4391-a882-1b9708840048.png)

- item_id(선택)
    - 하나의 강의에 여러 강의(Table of contents)가 있는 경우 강의를 구분하는 데 사용되는 식별자입니다.
    - 위 경우가 아니라면 **기본적으로 item_id는 필요로 하지 않습니다.**
- JSESSIONID(필수)
    - 사용자의 로그인 세션을 유지하기 위한 식별자입니다.
    - 로그인 세션이 살아있는 동안에는 변경되지 않기 때문에, 한 번 입력해놓으면 일일이 JSESSIONID를 확인할 필요가 없습니다.

## 사용법

0. exe 파일 실행 시 같은 폴더에 ui 파일이 위치해야 함

	a. (참고) exe 파일 실행 시 에러가 나는 경우 `main.py`  직접 실행

		i. python 3.9.7 버전 다운로드
    
		ii. pip install requests lxml bs4 PyQt5
    
		iii. python main.py

1. 다운로드할 과목의 이클래스 페이지로 진입

![Untitled](https://user-images.githubusercontent.com/76826021/172287962-0b1e280e-1a5d-4bb2-bb3a-6950730cd082.png)

2. 개발자 도구(F12 or ctrl+shift+I or 직접(크롬 도구 더보기 > 개발자 도구)) > Application(안 보이면 우측 '>>' 클릭) > Storage > Cookies 하위 항목 선택 후 JSESSIONID 확인

    - JSESSIONID는 한 번 설정해놓으면 로그아웃되지 않는 한, 바꿀 필요 없음

![Untitled 2](https://user-images.githubusercontent.com/76826021/172287908-d318905b-5364-4305-affc-bd8f97b00ac9.png)

2-1(선택). 개발자 도구를 켜고, 학습하기 클릭. 개발자 도구 > Network > Filter > acl 입력 후 Payload에서 item_id 확인.

   (Network 화면이 안 보일 시 ctrl+R)

   ![Untitled 3](https://user-images.githubusercontent.com/76826021/172287947-1962d059-f9c0-4ce5-855a-9e4db887152c.png)

3. 프로그램에 파일 이름, 저장 위치, lecture_weeks, item_id(선택), JSESSIONID를 입력하고 다운로드

## 유의사항

- 한국공학대학교 이클래스에 한해서만 사용 가능
- 일부 동영상은 다운로드 되지 않거나 오디오 파일만 다운로드 되는 경우가 존재함
- 분리된 동영상을 하나의 영상으로 병합하지는 않음

  이 때에는, 파일명 끝에 순번이 있기 때문에 인기 동영상 플레이어로 시청하기를 권함
