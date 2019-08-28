import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime

import Tracker
from Table import Table

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setFixedSize(1080, 768)
        self.table = Table(self)
        self.scale = None
        self.reference = None
        self.units = None
        self.points = []
        
        self.setCentralWidget(self.table)
        

    def referenceWindow(self):
        '''
        Displays window to enter lat/lon of reference point
        '''
        self.refWindow = Tracker.ReferencePoint(self)

    def setReference(self, point):
        '''
        Sets the local reference variable with point data passed from reference window
        '''
        self.reference = point

    def scaleWindow(self):
        '''
        Launches window to trace scale
        '''
        self.scaleWindow = Tracker.Tracker('scale', self)

    def setScale(self, scale, units):
        '''
        Sets Scale and unit input passed from scale window
        '''
        self.scale = scale
        self.units = units

    def locatorWindow(self):
        '''
        Launches window to locate new point from reference point
        '''
        if self.reference and self.scale and self.units:
            self.locatorWindow = Tracker.Tracker( 
                'locator', 
                self,
                ref=self.reference, 
                scale=self.scale, 
                units=self.units)

    def addLocation(self, lat, lon, desc):
        '''
        Adds location to points list and passes list to Table class to update table data
        '''
        data = {
            'lat': lat,
            'lon': lon,
            'date': QDateTime().currentDateTime(),
            'desc': desc
        }
        self.points.append(data)
        self.table.update(self.points)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())