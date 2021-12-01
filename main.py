import os.path
import sys
import traceback
import requests
from bs4 import BeautifulSoup
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5 import uic
import tkinter
from tkinter import filedialog
from PyQt5.QtCore import *
from enum import Enum
from exceptions import *

base_url_php = "http://cms.kpu.ac.kr/viewer/ssplayer/uniplayer_support/content.php?content_id={}"
base_url_media = "http://cms.kpu.ac.kr/contents6_pseudo/kpu1000001/{}/contents/media_files/{}"


class Status(Enum):
    READY = 1
    DOWNLOADING = 2
    ERR = 3


class SignalArgs:
    def __init__(self, status, exception=Exception('에러가 발생했습니다.')):
        self.status = status
        self.exception = exception


# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("myapp.ui")[0]


# 화면을 띄우는데 사용되는 Class 선언
def download_video(file_name_text, content_id_text, file_loc_text):
    url_php = base_url_php.format(content_id_text)
    print(url_php)
    res = requests.get(url_php)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        tds = soup.select('story_list > story > main_media_list > main_media')

        for idx, td in enumerate(tds):
            full_file_path = file_loc_text + '/' + file_name_text + '_' + str(idx) + '.mp4'
            print(full_file_path)
            if os.path.isfile(full_file_path):
                raise SameFileExists()
            url_media = base_url_media.format(content_id_text, td.text)
            urllib.request.urlretrieve(url_media, full_file_path)


class VideoDownloaderWorker(QThread):
    status = pyqtSignal(SignalArgs)

    def __init__(self, parent, file_name_text, content_id_text, file_loc_text):
        super().__init__(parent)

        self.file_name_text = file_name_text
        self.content_id_text = content_id_text
        self.file_loc_text = file_loc_text

    def run(self):
        self.status.emit(SignalArgs(status=Status.DOWNLOADING))
        try:
            download_video(file_name_text=self.file_name_text, content_id_text=self.content_id_text, file_loc_text=self.file_loc_text)
        except SameFileExists as e:
            self.status.emit(SignalArgs(status=Status.ERR, exception=e))
        except Exception:
            err = traceback.format_exc()
            print(str(err))
            self.status.emit(SignalArgs(status=Status.ERR))

        self.status.emit(SignalArgs(status=Status.READY))


class MyApp(QMainWindow, form_class):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setupUi(self)
        self.setFixedSize(491, 160)
        self.downloadButton.clicked.connect(self.download_btn_clicked)
        self.fileLocationButton.clicked.connect(self.file_location_btn_clicked)

    def initUI(self):
        self.statusBar().showMessage('준비 완료')

    @pyqtSlot(SignalArgs)
    def update_status(self, signal_args):
        if signal_args.status is Status.READY:
            self.statusBar().showMessage('준비 완료')
            self.fileNameEdit.setEnabled(True)
            self.contentIdEdit.setEnabled(True)
            self.fileLocationButton.setEnabled(True)
            self.downloadButton.setEnabled(True)
        elif signal_args.status is Status.DOWNLOADING:
            self.statusBar().showMessage('다운로드 중')
            self.fileNameEdit.setEnabled(False)
            self.contentIdEdit.setEnabled(False)
            self.fileLocationButton.setEnabled(False)
            self.downloadButton.setEnabled(False)
        elif signal_args.status is Status.ERR:
            QMessageBox(self).critical(self, '에러 발생', str(signal_args.exception))


    def download_btn_clicked(self):
        file_name_text = self.fileNameEdit.text()
        content_id_text = self.contentIdEdit.text()
        file_loc_text = self.fileLocationEdit.text()

        if file_name_text == '':
            QMessageBox(self).critical(self, '다운로드 할 수 없음', '파일 이름을 입력해주세요.')
            return

        if content_id_text == '':
            QMessageBox(self).critical(self, '다운로드 할 수 없음 ', '동영상 ID를 입력해주세요.')
            return

        if file_loc_text == '':
            QMessageBox(self).critical(self, '다운로드 할 수 없음 ', '저장 위치를 지정해주세요.')
            return

        th = VideoDownloaderWorker(self, file_name_text, content_id_text, file_loc_text)
        th.start()
        th.status.connect(self.update_status)

    def file_location_btn_clicked(self):
        root = tkinter.Tk()
        root.withdraw()
        dir_path = filedialog.askdirectory(parent=root, initialdir="/", title='동영상 저장 위치 지정')
        self.fileLocationEdit.setText(dir_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyApp()
    myWindow.show()
    app.exec_()