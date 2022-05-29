import os.path
import sys
import traceback
import requests
import lxml
import re
import json
from bs4 import BeautifulSoup

import urllib.request
from PyQt5.QtWidgets import *
from PyQt5 import uic
import tkinter
from tkinter import filedialog
from PyQt5.QtCore import *
from enum import Enum
from exceptions import *

base_url_php = "http://cms.tukorea.ac.kr/viewer/ssplayer/uniplayer_support/content.php?content_id={}"
base_url_php_media = "http://cms.tukorea.ac.kr/contents{}_pseudo/kpu1000001/{}/contents/media_files/{}"


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


def download_video_1(file_name_text, file_loc_text, content_id_text):
    downloaded = False
    url_php = base_url_php.format(content_id_text)
    print("url_php: {}".format(url_php))
    res = requests.get(url_php)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text)
        tds = soup.select('story_list > story > main_media_list > main_media')

        for idx, td in enumerate(tds):
            full_file_path = file_loc_text + '/' + file_name_text + '_' + str(idx) + '.mp4'
            print(full_file_path)
            if os.path.isfile(full_file_path):
                raise SameFileExists()
            for i in range(0, 101):
                try:
                    if i == 0:
                        url_media = base_url_php_media.format('', content_id_text, td.text)
                        urllib.request.urlretrieve(url_media, full_file_path)
                        downloaded = True

                    url_media = base_url_php_media.format(i, content_id_text, td.text)
                    urllib.request.urlretrieve(url_media, full_file_path)
                    downloaded = True
                    break
                except Exception:
                    continue

    return downloaded


def download_video_2(file_name_text, file_loc_text, content_id_text):
    downloaded = False
    url_php = base_url_php.format(content_id_text)
    print("url_php: {}".format(url_php))
    res = requests.get(url_php)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text)
        tds = soup.select('main_media > desktop > flash_fallback > media_uri')

        for idx, td in enumerate(tds):
            full_file_path = file_loc_text + '/' + file_name_text + '_' + str(idx) + '.mp4'
            print(full_file_path)
            if os.path.isfile(full_file_path):
                raise SameFileExists()
            try:
                url_media = td.text
                urllib.request.urlretrieve(url_media, full_file_path)
                downloaded = True
            except Exception:
                continue

    return downloaded


def download_video_3(file_name_text, file_loc_text, online_view_navi_response):

    if online_view_navi_response.status_code == 200:
        full_file_path = file_loc_text + '/' + file_name_text + '.mp4'
        print(full_file_path)
        if os.path.isfile(full_file_path):
            raise SameFileExists()
        urllib.request.urlretrieve(online_view_navi_response.json()["path"], full_file_path)

        return True

    return False


def online_view_form(lecture_weeks_text, item_id_text, jsession_id_text):

    cookies = {'JSESSIONID': jsession_id_text, '_language_': 'ko'}

    response = requests.post('http://eclass.tukorea.ac.kr/ilos/st/course/online_view_form.acl',
                             data={'lecture_weeks': lecture_weeks_text, 'item_id': item_id_text},
                             cookies=cookies)

    matched = re.search(r'cv\.load(\((.*?)\));', response.text, re.S)

    params = list(map(lambda str : str.strip().strip("\""), matched.group(2).split(",")))

    return {
        "navi": params[0],
        "item_id": params[1],
        "content_id": params[2],
        "organization_id": params[3],
        "lecture_weeks": params[4],
        "ky": params[5],
        "ud": params[6],
    }


def online_view_navi(online_view_form_json, jsession_id_text):

    cookies = {'JSESSIONID': jsession_id_text, '_language_': 'ko'}

    return requests.post('http://eclass.tukorea.ac.kr/ilos/st/course/online_view_navi.acl',
                             data={
                                 'navi': online_view_form_json["navi"],
                                 'item_id': online_view_form_json["item_id"],
                                 'content_id': online_view_form_json["content_id"],
                                 'organization_id': online_view_form_json["organization_id"],
                                 'lecture_weeks': online_view_form_json["lecture_weeks"],
                                 'ky': online_view_form_json["ky"],
                                 'ud': online_view_form_json["ud"],
                                 'returnData': "json",
                                 'encoding': "utf-8"
                             },
                             cookies=cookies)


class VideoDownloaderWorker(QThread):
    status = pyqtSignal(SignalArgs)

    def __init__(self, parent, file_name_text, file_loc_text, lecture_weeks_text, item_id_text, jsession_id_text):
        super().__init__(parent)

        self.file_name_text = file_name_text
        self.file_loc_text = file_loc_text
        self.lecture_weeks_text = lecture_weeks_text
        self.item_id_text = item_id_text
        self.jsession_id_text = jsession_id_text

    def run(self):
        self.status.emit(SignalArgs(status=Status.DOWNLOADING))
        try:

            online_view_form_json = online_view_form(self.lecture_weeks_text, self.item_id_text, self.jsession_id_text)
            online_view_navi_response = online_view_navi(online_view_form_json, self.jsession_id_text)

            content_id_text = online_view_navi_response.json()["path"].rsplit('/', 1)[-1]

            if download_video_1(file_name_text=self.file_name_text, file_loc_text=self.file_loc_text, content_id_text=content_id_text):
                self.status.emit(SignalArgs(status=Status.READY))
                return

            if download_video_2(file_name_text=self.file_name_text, file_loc_text=self.file_loc_text, content_id_text=content_id_text):
                self.status.emit(SignalArgs(status=Status.READY))
                return

            if download_video_3(file_name_text=self.file_name_text, file_loc_text=self.file_loc_text, online_view_navi_response=online_view_navi_response):
                self.status.emit(SignalArgs(status=Status.READY))
                return

            self.status.emit(SignalArgs(status=Status.READY))

        except SameFileExists as e:
            self.status.emit(SignalArgs(status=Status.ERR, exception=e))
        except Exception:
            err = traceback.format_exc()
            self.status.emit(SignalArgs(status=Status.ERR, exception=err))


class MyApp(QMainWindow, form_class):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setupUi(self)
        self.setFixedSize(491, 188)
        self.downloadButton.clicked.connect(self.download_btn_clicked)
        self.fileLocationButton.clicked.connect(self.file_location_btn_clicked)

    def initUI(self):
        self.statusBar().showMessage('준비 완료')

    @pyqtSlot(SignalArgs)
    def update_status(self, signal_args):
        if signal_args.status is Status.READY:
            self.statusBar().showMessage('준비 완료')
            self.fileNameEdit.setEnabled(True)
            self.fileLocationButton.setEnabled(True)
            self.lectureWeeksEdit.setEnabled(True)
            self.itemIdEdit.setEnabled(True)
            self.jsessionIdEdit.setEnabled(True)
            self.downloadButton.setEnabled(True)
        elif signal_args.status is Status.DOWNLOADING:
            self.statusBar().showMessage('다운로드 중')
            self.fileNameEdit.setEnabled(False)
            self.fileLocationButton.setEnabled(False)
            self.lectureWeeksEdit.setEnabled(False)
            self.itemIdEdit.setEnabled(False)
            self.jsessionIdEdit.setEnabled(False)
            self.downloadButton.setEnabled(False)
        elif signal_args.status is Status.ERR:
            QMessageBox(self).critical(self, '에러 발생', str(signal_args.exception))
            self.statusBar().showMessage('준비 완료')
            self.fileNameEdit.setEnabled(True)
            self.fileLocationButton.setEnabled(True)
            self.lectureWeeksEdit.setEnabled(True)
            self.itemIdEdit.setEnabled(True)
            self.jsessionIdEdit.setEnabled(True)
            self.downloadButton.setEnabled(True)


    def download_btn_clicked(self):
        file_name_text = self.fileNameEdit.text()
        file_loc_text = self.fileLocationEdit.text()
        lecture_weeks_text = self.lectureWeeksEdit.text()
        item_id_text = self.itemIdEdit.text()
        jsession_id_text = self.jsessionIdEdit.text()

        if file_name_text == '':
            QMessageBox(self).critical(self, '다운로드 할 수 없음', '파일 이름을 입력해주세요.')
            return

        if file_loc_text == '':
            QMessageBox(self).critical(self, '다운로드 할 수 없음 ', '저장 위치를 지정해주세요.')
            return

        if lecture_weeks_text == '':
            QMessageBox(self).critical(self, '다운로드 할 수 없음 ', 'lecture_weeks를 입력해주세요.')
            return

        if item_id_text == '':
            QMessageBox(self).critical(self, '다운로드 할 수 없음 ', 'item_id를 입력해주세요.')
            return

        if jsession_id_text == '':
            QMessageBox(self).critical(self, '다운로드 할 수 없음 ', 'JSESSIONID를 입력해주세요.')
            return

        th = VideoDownloaderWorker(self, file_name_text, file_loc_text, lecture_weeks_text, item_id_text, jsession_id_text)
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