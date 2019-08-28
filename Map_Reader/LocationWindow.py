import sys
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from geopy.distance import geodesic
from collections import namedtuple
import math

#Class to confirm lat, lon data
class LocationWindow(QWidget):
    def __init__(self, lat, lon, parent):
        super(LocationWindow, self).__init__()
        self.lat = lat
        self.lon = lon
        self.parent = parent

        #self.setFixedSize(300, 100)
        self.setWindowTitle('Confirm Location')
        self.initUI()

    def initUI(self):
        '''
        Setup GUI elements of scale window
        '''
        mainLayout = QVBoxLayout()

        #horizontal layout containing lineedits, unit selector, and label
        hLayout = QHBoxLayout() 
        self.latEdit = QLineEdit(str(self.lat))
        self.latEdit.setValidator(QtGui.QDoubleValidator(-90, 90, 5)) 
        self.lonEdit = QLineEdit(str(self.lon))
        self.lonEdit.setValidator(QtGui.QDoubleValidator(-180, 180, 5))    

        hLayout.addWidget(QLabel('Lat:'))
        hLayout.addWidget(self.latEdit)

        hLayout.addWidget(QLabel('Lon:'))
        hLayout.addWidget(self.lonEdit)

        #add description box
        self.descBox = QTextEdit()
        self.descBox.setFixedHeight(100)
        self.descBox.setPlaceholderText('Description')

        #horizontal layout containing save and cancel buttons
        h2Layout = QHBoxLayout()
        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.save)

        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancel)

        h2Layout.addWidget(self.saveButton)
        h2Layout.addWidget(self.cancelButton)

        mainLayout.addLayout(hLayout)
        mainLayout.addWidget(self.descBox)
        mainLayout.addLayout(h2Layout)
    
        self.setLayout(mainLayout)

    def save(self):
        '''
        Send scale and unit values entered by user back to mouse mainwindow
        screen when save button is clicked.
        '''
        #Get text values from each element
        lat = eval(self.latEdit.text())
        lon = eval(self.lonEdit.text())
        desc = self.descBox.toPlainText()
        
        #check values entered by user are correct
        if lat > -90 and lat < 90 and lon > -180 and lon < 180:
            self.parent.setLocation(lat, lon, desc)
            self.close()

    def cancel(self):
        '''
        Return to mouse tracker screen if cancel button is clicked
        '''
        self.close()