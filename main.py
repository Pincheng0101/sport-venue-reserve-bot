import sys
import time
import json
from datetime import datetime, timedelta

from PyQt6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget,
                             QLabel, QLineEdit, QPushButton, QPlainTextEdit, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer

from badminton import Badminton


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # default
        self.upid = ''
        self.username = ''
        self.phonenumber = ''
        self.venue = '大安'
        self.land = '3F羽球10'
        self.date = '2022-11-19'
        self.start_time = '20:00'
        self.end_time = '21:00'
        self.start_reserve_time = (datetime.strptime(self.date, '%Y-%m-%d') - timedelta(days=13, seconds=5)).timestamp()

        self.resize(600, 500)
        self.setWindowTitle("運動中心預定系統")

        self.font = QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(20)

        page_layout = QVBoxLayout()
        upid_layout = QHBoxLayout()
        username_layout = QHBoxLayout()
        phonenumber_layout = QHBoxLayout()
        venue_layout = QHBoxLayout()
        land_layout = QHBoxLayout()
        date_layout = QHBoxLayout()
        start_time_layout = QHBoxLayout()
        end_time_layout = QHBoxLayout()

        page_layout.addLayout(upid_layout)
        page_layout.addLayout(username_layout)
        page_layout.addLayout(phonenumber_layout)
        page_layout.addLayout(venue_layout)
        page_layout.addLayout(land_layout)
        page_layout.addLayout(date_layout)
        page_layout.addLayout(start_time_layout)
        page_layout.addLayout(end_time_layout)

        upid_layout.addWidget(self.label("UPID：      "))
        self.upid_input = self.input(self.upid)
        upid_layout.addWidget(self.upid_input)

        username_layout.addWidget(self.label("名稱：       "))
        self.username_input = self.input(self.username)
        username_layout.addWidget(self.username_input)

        phonenumber_layout.addWidget(self.label("電話：       "))
        self.phonenumber_input = self.input(self.phonenumber)
        phonenumber_layout.addWidget(self.phonenumber_input)

        venue_layout.addWidget(self.label("地點：       "))
        self.venue_input = self.input(self.venue)
        venue_layout.addWidget(self.venue_input)

        land_layout.addWidget(self.label("場地：       "))
        self.land_input = self.input(self.land)
        land_layout.addWidget(self.land_input)

        date_layout.addWidget(self.label("日期：       "))
        self.date_input = self.input(self.date)
        date_layout.addWidget(self.date_input)

        start_time_layout.addWidget(self.label("開始時間："))
        self.start_time_input = self.input(self.start_time)
        start_time_layout.addWidget(self.start_time_input)

        end_time_layout.addWidget(self.label("結束時間："))
        self.end_time_input = self.input(self.end_time)
        end_time_layout.addWidget(self.end_time_input)

        reserve_button = self.button("預約", self.start_reserve)
        page_layout.addWidget(reserve_button)

        self.result_textarea = QPlainTextEdit()
        textarea_font = QFont()
        textarea_font.setFamily("Arial")
        textarea_font.setPointSize(16)
        self.result_textarea.setFont(textarea_font)
        self.result_textarea.resize(400, 200)
        page_layout.addWidget(self.result_textarea)

        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

    def toDateTime(self, t):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

    def label(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.adjustSize()
        label.setFont(self.font)
        return label

    def input(self, default_text=""):
        input = QLineEdit()
        input.setText(default_text)
        input.setAlignment(Qt.AlignmentFlag.AlignRight)
        input.adjustSize()
        input.setFont(self.font)
        return input

    def button(self, text, method):
        button = QPushButton(text)
        button.setFont(self.font)
        button.clicked.connect(method)
        return button

    def start_reserve(self):
        if self.upid_input.text() == "":
            QMessageBox.about(self, "輸入錯誤", "請輸入UPID")
            return
        if self.username_input.text() == "":
            QMessageBox.about(self, "輸入錯誤", "請輸入名稱")
            return
        if self.phonenumber_input.text() == "":
            QMessageBox.about(self, "輸入錯誤", "請輸入電話")
            return
        if self.venue_input.text() == "":
            QMessageBox.about(self, "輸入錯誤", "請輸入地點")
            return
        if self.land_input.text() == "":
            QMessageBox.about(self, "輸入錯誤", "請輸入場地")
            return
        if self.date_input.text() == "":
            QMessageBox.about(self, "輸入錯誤", "請輸入日期")
            return
        if self.start_time_input.text() == "":
            QMessageBox.about(self, "輸入錯誤", "請輸入開始時間")
            return
        if self.end_time_input.text() == "":
            QMessageBox.about(self, "輸入錯誤", "請輸入結束時間")
            return

        self.init_badminton()
        self.wait_loop()

    def init_badminton(self):
        self.badminton = Badminton(
            # universally unique id
            uuid='43820D38-282F-4ECE-92DD-AE5B777AC892',
            # user personal id
            upid=self.upid_input.text(),
            username=self.username_input.text(),
            phonenumber=self.phonenumber_input.text(),
        )
        self.username = self.username_input.text()
        self.phonenumber = self.phonenumber_input.text()
        self.venue = self.venue_input.text()
        self.land = self.land_input.text()
        self.date = self.date_input.text()
        self.start_time = self.start_time_input.text()
        self.end_time = self.end_time_input.text()
        self.start_reserve_time = (datetime.strptime(self.date, '%Y-%m-%d') - timedelta(days=13, seconds=5)).timestamp()

    def wait_loop(self):
        self.set_message()
        now = time.time()
        if now < self.start_reserve_time:
            QTimer.singleShot(1000, lambda: self.wait_loop())
        else:
            self.reserve_loop()

    def reserve_loop(self):
        now = time.time()
        if now > self.start_reserve_time:
            result = self.badminton.reserve_location(self.venue, self.land, self.date, self.start_time, self.end_time)
            if result['Data']['Status'] == "1":
                self.append_message(f"{self.toDateTime(now)} 預約成功")
            else:
                self.append_message(f"{self.toDateTime(now)} 預約失敗")
                QTimer.singleShot(200, lambda: self.reserve_loop())

    def set_message(self):
        now = time.time()
        self.result_textarea.clear()
        self.append_message(f"------------------------------------------------------")
        self.append_message(f"目前時間: {self.toDateTime(now)}")
        self.append_message(f"開始預約時間: {self.toDateTime(self.start_reserve_time)}")
        self.append_message(f"預約場地: {self.venue} {self.land}")
        self.append_message(f"預約日期: {self.date}")
        self.append_message(f"開始時間: {self.start_time}")
        self.append_message(f"結束時間: {self.end_time}")
        self.append_message(f"------------------------------------------------------")

    def append_message(self, text):
        self.result_textarea.appendPlainText(text)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
