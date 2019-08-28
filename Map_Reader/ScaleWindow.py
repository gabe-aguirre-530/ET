import sys
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from geopy.distance import geodesic
from collections import namedtuple
import math

#Class to confirm the scale input data
class ScaleWindow(QWidget):
    def __init__(self, dist_px, parent):
        super(ScaleWindow, self).__init__()

        self.dist_px = dist_px
        self.scale = 1
        self.parent = parent

        self.setFixedSize(300, 100)
        self.setWindowTitle('Scale')
        self.initUI()

    def initUI(self):
        '''
        Setup GUI elements of scale window
        '''
        mainLayout = QVBoxLayout()

        #horizontal layout containing lineedits, unit selector, and label
        hLayout = QHBoxLayout() 
        self.pixelEdit = QLineEdit(str(self.dist_px))
        self.pixelEdit.setValidator(QtGui.QDoubleValidator(0.99, 1000.00, 2)) 
        self.scaleEdit = QLineEdit(str(self.scale))
        self.scaleEdit.setValidator(QtGui.QDoubleValidator(0.99, 1000.00, 2))    

        label = QLabel('Pixels:')

        units = ['km', 'm', 'ft', 'nm']
        self.comboBox = QComboBox()
        self.comboBox.addItems(units)

        hLayout.addWidget(label)
        hLayout.addWidget(self.pixelEdit)
        hLayout.addWidget(self.scaleEdit)
        hLayout.addWidget(self.comboBox)

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

    def save(self):
        '''
        Send scale and unit values entered by user back to mouse tracker
        screen when save button is clicked.
        '''
        #Get text values from each element
        scale = eval(self.scaleEdit.text())
        dist_px = eval(self.pixelEdit.text())
        units = self.comboBox.currentText()
        
        #check values entered by user are correct
        if scale > 0 and dist_px > 0:
            pxPerUnit = dist_px / scale
            self.parent.setScale(pxPerUnit, units)        
            self.close()

    def cancel(self):
        '''
        Return to mouse tracker screen if cancel button is clicked
        '''
        self.close()