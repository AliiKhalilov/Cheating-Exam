import cv2
import numpy as np
import tensorflow as tf
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QListWidget, QVBoxLayout, QLabel, QPushButton
import sys

# Load your model
model = tf.keras.models.load_model("test_cheat.h5")

class Ui_UploadDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("UploadDialog")
        Dialog.resize(1121, 761)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(-10, -20, 1200, 800))
        self.widget.setStyleSheet("QWidget#widget{\n"
                                  "background-color:rgb(0, 0, 83);}")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(260, 50, 601, 81))
        self.label.setStyleSheet("font: 75 28pt \"MS Shell Dlg 2\"; color:rgb(255, 255, 255)")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(60, 70, 71, 51))
        self.label_2.setStyleSheet("background-color: rgb(0, 0, 107);")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../../../Downloads/1630473458687.jpeg"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(50, 630, 601, 81))
        self.label_3.setStyleSheet("font: 75 20pt \"MS Shell Dlg 2\"; color:rgb(255, 255, 255)")
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(750, 650, 131, 41))
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(20, 230, 1101, 81))
        self.label_4.setStyleSheet("font: 75 18pt \"MS Shell Dlg 2\"; color:rgb(255, 255, 255)")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(20, 310, 1101, 81))
        self.label_5.setStyleSheet("font: 75 18pt \"MS Shell Dlg 2\"; color:rgb(255, 255, 255)")
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("UploadDialog", "Upload Video"))
        self.label.setText(_translate("UploadDialog", "Welcome Caspian Local App"))
        self.label_3.setText(_translate("UploadDialog", "Please upload video for checking "))
        self.pushButton.setText(_translate("UploadDialog", "Upload"))
        self.label_4.setText(_translate("Dialog", "The recent observation is that people tend to attempt cheating during online exams."))
        self.label_5.setText(_translate("Dialog", "That is why We decide to detect these actions with helping AI"))

class Ui_ResultDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("ResultDialog")
        Dialog.resize(1121, 761)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1121, 761))
        self.widget.setStyleSheet("QWidget#widget{\n"
                                  "background-color:rgb(0, 0, 83);}")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(260, 50, 601, 81))
        self.label.setStyleSheet("font: 75 28pt \"MS Shell Dlg 2\"; color:rgb(255, 255, 255)")
        self.label.setObjectName("label")
        self.result_list = QListWidget(self.widget)
        self.result_list.setGeometry(QtCore.QRect(20, 150, 1081, 200))
        self.result_list.setStyleSheet("font: 12pt \"MS Shell Dlg 2\"; color:rgb(0, 0, 0)")
        self.result_list.setObjectName("result_list")
        self.label.setText("Video Analysis Results")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("ResultDialog", "Results"))

class VideoUploadDialog(QDialog, Ui_UploadDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.upload_video)
        self.video_file = None

    def upload_video(self):
        self.video_file, _ = QFileDialog.getOpenFileName(self, 'Select Video')
        if self.video_file:
            self.accept()  # Close the upload dialog and accept the file

class VideoResultDialog(QDialog, Ui_ResultDialog):
    def __init__(self, video_file):
        super().__init__()
        self.setupUi(self)
        self.video_file = video_file
        self.process_video()

    def process_video(self):
        if self.video_file:
            cap = cv2.VideoCapture(self.video_file)

            cheat_times = []
            normal_times = []
            frame_count = 0
            frame_rate = cap.get(cv2.CAP_PROP_FPS)
            frame_skip_interval = 5

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1

                if frame_count % frame_skip_interval != 0:
                    continue

                resize = cv2.resize(frame, (256, 256))
                yhat = model.predict(np.expand_dims(resize / 255, 0))
                if yhat > 0.5:
                    normal_times.append(frame_count / frame_rate)
                else:
                    cheat_times.append(frame_count / frame_rate)

            cap.release()

            cheat_seconds = list(set(int(time) for time in cheat_times))
            normal_seconds = list(set(int(time) for time in normal_times))
            if 0 in cheat_seconds:
                cheat_seconds.remove(0)
            if 0 in normal_seconds:
                normal_seconds.remove(0)
            self.show_result(cheat_seconds, normal_seconds)

    def show_result(self, cheat_seconds, normal_seconds):
        self.result_list.clear()
        cheat_updated = [self.format_time(sec) for sec in cheat_seconds]
        normal_updated = [self.format_time(sec) for sec in normal_seconds]
        for i in cheat_updated:
            if i in normal_updated:
                normal_updated.remove(i)
        self.result_list.addItem('Cheat Seconds:')
        self.result_list.addItems(cheat_updated)
        self.result_list.addItem('Normal Seconds:')
        self.result_list.addItems(normal_updated)

    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    upload_dialog = VideoUploadDialog()
    if upload_dialog.exec_() == QDialog.Accepted:
        video_file = upload_dialog.video_file
        result_dialog = VideoResultDialog(video_file)
        result_dialog.exec_()

    sys.exit(app.exec_())
