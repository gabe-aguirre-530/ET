import sys
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from geopy.distance import geodesic
from collections import namedtuple
import math

#Class to confirm the reference point data
class ReferenceWindow(QWidget):
    def __init__(self, parent):
        super(ReferenceWindow, self).__init__()
        self.parent = parent
        self.setFixedSize(300, 100)
        self.setWindowTitle('Add Reference Point')
        self.initUI()

    def initUI(self):
        '''
        Setup GUI elements of scale window
        '''
        mainLayout = QVBoxLayout()

        #horizontal layout containing lineedits, unit selector, and label
        hLayout = QHBoxLayout() 
        self.latEdit = QLineEdit()
        self.latEdit.setValidator(QtGui.QDoubleValidator(-90, 90, 5))
        self.latEdit.setPlaceholderText('Latitude')

        self.lonEdit = QLineEdit()
        self.lonEdit.setValidator(QtGui.QDoubleValidator(-180, 180, 5))
        self.lonEdit.setPlaceholderText('Longitude')

        hLayout.addWidget(self.latEdit)
        hLayout.addWidget(self.lonEdit)

        #horizontal layout containing save and cancel buttons
        h2Layout = QHBoxLayout()
        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.save)

        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancel)

        h2Layout.addWidget(self.saveButton)
        h2Layout.addWidget(self.cancelButton)

        mainLayout.addLayout(hLayout)
        mainLayout.addLayout(h2Layout)
    
        self.setLayout(mainLayout)

        self.show()

    def save(self):
        '''
        Send reference point back to main window to be stored
        '''
        #Get text values from each element
        lat = eval(self.latEdit.text())
        lon = eval(self.lonEdit.text())
        
        #check values entered by user are correct
        if lat > -90 and lat < 90 and lon > -180 and lon < 180:
            self.parent.setReference((lat, lon))
            self.close()

    def cancel(self):
        '''
        Return to mouse tracker screen if cancel button is clicked
        '''
        self.close()