class SameFileExists(Exception):    # Exception을 상속받아서 새로운 예외를 만듦
    def __init__(self):
        super().__init__('같은 이름의 파일이 이미 존재합니다.')