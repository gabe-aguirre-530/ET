from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDoubleValidator
from geopy.distance import geodesic
from collections import namedtuple

#Class to confirm the scale input data
class ScaleWindow(QDialog):
    def __init__(self, dist_px, parent):
        super(ScaleWindow, self).__init__(parent)

        self.dist_px = dist_px
        self.scale = 1

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
        self.pixelEdit.setValidator(QDoubleValidator(0.99, 1000.00, 2)) 
        self.scaleEdit = QLineEdit(str(self.scale))
        self.scaleEdit.setValidator(QDoubleValidator(0.99, 1000.00, 2))    

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
        self.show()

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
            self.parent().setScale(pxPerUnit, units)        
            self.close()

    def cancel(self):
        '''
        Return to mouse tracker screen if cancel button is clicked
        '''
        self.close()
        
#Class to confirm the reference point data
class ReferenceWindow(QDialog):
    def __init__(self, parent):
        super(ReferenceWindow, self).__init__(parent)
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
        self.latEdit.setValidator(QDoubleValidator(-90, 90, 5))
        self.latEdit.setPlaceholderText('Latitude')
        self.latEdit.textChanged.connect(self.checkFields)

        self.lonEdit = QLineEdit()
        self.lonEdit.setValidator(QDoubleValidator(-180, 180, 5))
        self.lonEdit.setPlaceholderText('Longitude')
        self.lonEdit.textChanged.connect(self.checkFields)

        hLayout.addWidget(self.latEdit)
        hLayout.addWidget(self.lonEdit)

        #horizontal layout containing save and cancel buttons
        h2Layout = QHBoxLayout()
        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.save)
        self.saveButton.setEnabled(False)

        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancel)

        h2Layout.addWidget(self.saveButton)
        h2Layout.addWidget(self.cancelButton)

        mainLayout.addLayout(hLayout)
        mainLayout.addLayout(h2Layout)
    
        self.setLayout(mainLayout)

        self.show()

    def checkFields(self):
        if self.lonEdit.text() and self.latEdit.text():
            self.saveButton.setEnabled(True)

    def save(self):
        '''
        Send reference point back to main window to be stored
        '''
        #Get text values from each element
        lat = eval(self.latEdit.text())
        lon = eval(self.lonEdit.text())
        
        #check values entered by user are correct
        if lat > -90 and lat < 90 and lon > -180 and lon < 180:
            self.parent().setReference((lat, lon))
            self.close()

    def cancel(self):
        '''
        Return to mouse tracker screen if cancel button is clicked
        '''
        self.close()
        
#Class to confirm lat, lon data
class LocationWindow(QDialog):
    def __init__(self, lat, lon, dist, bearing, units, parent):
        super(LocationWindow, self).__init__(parent)
        self.lat = lat
        self.lon = lon
        self.dist = dist
        self.bearing = bearing
        self.units = units

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
        self.latEdit.setValidator(QDoubleValidator(-90, 90, 5)) 
        self.lonEdit = QLineEdit(str(self.lon))
        self.lonEdit.setValidator(QDoubleValidator(-180, 180, 5))    

        hLayout.addWidget(QLabel('Lat:'))
        hLayout.addWidget(self.latEdit)

        hLayout.addWidget(QLabel('Lon:'))
        hLayout.addWidget(self.lonEdit)

        #add description box
        self.descBox = QTextEdit()
        self.descBox.setFixedHeight(100)
        self.descBox.setPlaceholderText('Description')

        h2Layout = QHBoxLayout() 

        self.distEdit = QLineEdit(str(self.dist))
        self.distEdit.setValidator(QDoubleValidator(0.1, 100000000, 5)) 
        self.bearingEdit = QLineEdit(str(self.bearing))
        self.bearingEdit.setValidator(QDoubleValidator(0, 360, 5))

        h2Layout.addWidget(QLabel(f'Distance ({self.units}):'))
        h2Layout.addWidget(self.distEdit)

        h2Layout.addWidget(QLabel('Bearing:'))
        h2Layout.addWidget(self.bearingEdit)

        #horizontal layout containing save and cancel buttons
        h3Layout = QHBoxLayout()
        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.save)

        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancel)

        h3Layout.addWidget(self.saveButton)
        h3Layout.addWidget(self.cancelButton)

        mainLayout.addLayout(hLayout)
        mainLayout.addLayout(h2Layout)
        mainLayout.addWidget(self.descBox)
        mainLayout.addLayout(h3Layout)
    
        self.setLayout(mainLayout)
        self.show()

    def save(self):
        '''
        Send scale and unit values entered by user back to mouse mainwindow
        screen when save button is clicked.
        '''
        #Get text values from each element
        lat = eval(self.latEdit.text())
        lon = eval(self.lonEdit.text())
        desc = self.descBox.toPlainText()
        dist = eval(self.distEdit.text())
        bearing = eval(self.bearingEdit.text())
        units = self.units
        
        #check values entered by user are correct
        if lat > -90 and lat < 90 and lon > -180 and lon < 180:
            self.parent().setLocation(lat, lon, desc, dist, bearing, units)
            self.close()

    def cancel(self):
        '''
        Return to mouse tracker screen if cancel button is clicked
        '''
        self.close()