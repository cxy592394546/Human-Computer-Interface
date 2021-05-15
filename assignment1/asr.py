import os
import sys
import re
import time
import threading
import pyautogui
import speech_recognition as sr
from PyQt5 import QtWidgets, QtGui, QtCore

from asrInterface import Ui_MainWindow


class myWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.button.clicked.connect(self.create_thread)

    def create_thread(self):
        self.ui.label.setText("Recognising, please speak!")
        t = threading.Thread(target=self.recognize)
        t.setDaemon(True)
        t.start()

    def recognize(self):
        mic = sr.Recognizer()
        with sr.Microphone() as source:
            audio = mic.listen(source)
        try:
            content = mic.recognize_sphinx(audio)
        except sr.RequestError:
            self.ui.label.setText("Please Try Again!")
            time.sleep(5)

        print("You say:" + content)
        self.match_mic(content)

    def match_mic(self, content):
        menu = ["mu", "fi", "sh"]
        play_music = re.search(menu[0].lower(), content.lower())
        open_file = re.search(menu[1].lower(), content.lower())
        screenshot = re.search(menu[2].lower(), content.lower())
        if play_music:
            self.ui.label.setText("Play Music!")
            os.system('music.m4a')
        elif open_file:
            self.ui.label.setText("Open File!")
            os.system("file.txt")
        elif screenshot:
            self.ui.label.setText("Screenshot After 10s!")
            time.sleep(10)
            img = pyautogui.screenshot()
            img.save("screenshot.jpg")
        else:
            self.ui.label.setText("Couldn't recognize, please try again!")
        time.sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = myWindow()
    application.show()
    sys.exit(app.exec())
