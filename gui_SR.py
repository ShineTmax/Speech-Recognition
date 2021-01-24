import sys
import os

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.Qt import *
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtGui import QFontMetrics, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QTextEdit, QPushButton, QScrollArea


import sounddevice as sd 
from scipy.io.wavfile import write 
import wavio as wv 
import speech_recognition as sr

import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
import pandas as pd

## Pour l'inco dans le TaskBar en bas
import ctypes
myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
##

class Menu(QMainWindow):

    def __init__(self):
        super().__init__()

        self.freq = 44100 # Sampling frequency 
        self.duration = 15 # Recording duration max

        self.running = None

        self.filename = False # variable qui permet de savoir si on fait showtext sur un fichier en particulier ou sur celui par défaut

        self.widget = QWidget(self)

        self.setWindowTitle("Voice recognition")

        #scriptDir = os.path.dirname(os.path.realpath(__file__))
        #self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo.png'))
        self.setWindowIcon(QIcon("img" + os.path.sep  + '001-microphone.png')) 

        self.central_widget = QWidget()               
        self.setCentralWidget(self.central_widget)    
        lay = QVBoxLayout(self.central_widget)
        
        label = QLabel(self)
        pixmap = QPixmap("img" + os.path.sep + "013-speak.png")
        pixmap = pixmap.scaled(409,409)
        label.setPixmap(pixmap)
        lay.addWidget(label)

        self.createHorizontalLayout()
        lay.addWidget(self.horizontalGroupBox)

        self.edit = QTextEdit()
        self.edit.resize(400,50)
        lay.addWidget(self.edit)
        
        self.createHorizontalLayout__2_()
        lay.addWidget(self.horizontalGroupBox)

        saveFile = QAction("&Save File", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.Save_text)

        self.show()



    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QHBoxLayout()
        
        buttonBlue = QPushButton('Start recording', self)
        buttonBlue.clicked.connect(self.start_recording)
        layout.addWidget(buttonBlue)
        
        buttonRed = QPushButton('Stop recording', self)
        buttonRed.clicked.connect(self.stop_recording)
        layout.addWidget(buttonRed)
        
        buttonGreen = QPushButton('Show text', self)
        buttonGreen.clicked.connect(self.show_text)
        layout.addWidget(buttonGreen)
        
        self.horizontalGroupBox.setLayout(layout)

    def start_recording(self):
        print("start it ...")
        if self.running is not None:
            print('already running')
        else:
            self.running = sd.rec(int(self.duration * self.freq), samplerate=self.freq, channels=1) 

    def stop_recording(self): 
        print("stop it ...")
        if self.running is not None:
            # Convert the NumPy array to audio file 
            wv.write("recording1.wav", self.running, self.freq, sampwidth=2)
            self.running = None
        else:
            print('not running') 

    def show_text(self): 
        r = sr.Recognizer()
        print("show text ...")
        print("filename = ",self.filename)
        if(self.filename == False):
            file = sr.AudioFile('recording1.wav')
        else:
            file = sr.AudioFile(self.filename)
        with file as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
            result = r.recognize_google(audio,language='en')
            #print(result)
        self.edit.clear()
        self.edit.append(result)

    def createHorizontalLayout__2_(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QHBoxLayout()

        buttonRed = QPushButton('Open Audio file', self)
        buttonRed.clicked.connect(self.Open_audio_file)
        layout.addWidget(buttonRed)
        
        buttonBlue = QPushButton('Save text', self)
        buttonBlue.clicked.connect(self.Save_text)
        layout.addWidget(buttonBlue)
        
        
        button_quit = QPushButton('Quit', self)
        button_quit.clicked.connect(self.quit)
        layout.addWidget(button_quit)
        
        self.horizontalGroupBox.setLayout(layout)

    def Open_audio_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        try:
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Audio file (*.wav);;Audio file (*.flac);; Audio file(.mp3)", options=options)
        except:
            print("##No audio file opened")
        if fileName:
            print(fileName.split('/')[-1])
            self.filename = fileName.split('/')[-1]
            QtMultimedia.QSound.play(self.filename)
            self.show_text()
            self.filename = False


    def Save_text(self):
        name = QFileDialog.getSaveFileName(self, 'Save File',"", "Text files (*.txt)")
        text = self.edit.toPlainText()
        try:
            file = open(name[0],'w')
            file.write(text)
            file.close()
        except:
            print("**No file Saved**")

    def quit(self):
        QCoreApplication.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())