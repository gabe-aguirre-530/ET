import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime, QDate
import pandas as pd

import Tracker
from Table import Table
from ReferenceWindow import *
from ScaleWindow import *
from LocationWindow import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setFixedSize(1080, 768)
        self.table = Table(self)
        self.scale = None
        self.reference = None
        self.units = None
        self.points = []
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        
        self.exportMenu = QMenu('Export', self)
        self.exportMenu.setEnabled(False)
        
        self.exportCSV = QAction('CSV', self)
        self.exportMenu.addAction(self.exportCSV)
        self.exportCSV.triggered.connect(self.exportToCSV)

        self.exportJSON = QAction('JSON', self)
        self.exportMenu.addAction(self.exportJSON)
        self.exportJSON.triggered.connect(self.exportToJSON)

        self.exportExcel = QAction('Excel', self)
        self.exportMenu.addAction(self.exportExcel)
        self.exportExcel.triggered.connect(self.exportToExcel)

        self.exportHTML = QAction('HTML', self)
        self.exportMenu.addAction(self.exportHTML)
        self.exportHTML.triggered.connect(self.exportToHTML)

        fileMenu.addMenu(self.exportMenu)
        self.setCentralWidget(self.table)
        

    def referenceWindow(self):
        '''
        Displays window to enter lat/lon of reference point
        '''
        self.refWindow = ReferenceWindow(self)

    def setReference(self, point):
        '''
        Sets the local reference variable with point data passed from reference window
        '''
        self.reference = point

    def scaleTracker(self):
        '''
        Launches window to trace scale
        '''
        self.scaleTracker = Tracker.Tracker('scale', self)

    def confirmScale(self, dist_px):
        '''
        Launches window to confirm scale data
        '''
        self.scaleConfirm = ScaleWindow(dist_px, self)
        self.scaleConfirm.show()

    def setScale(self, scale, units):
        '''
        Sets Scale and unit input passed from scale window
        '''
        self.scale = scale
        self.units = units
        self.scaleTracker.close()

    def locationTracker(self):
        '''
        Launches window to locate new point from reference point
        '''
        if self.reference and self.scale and self.units:
            self.locationTracker = Tracker.Tracker( 
                'location', 
                self,
                ref=self.reference, 
                scale=self.scale, 
                units=self.units)

    def confirmLocation(self, lat, lon):
        '''
        Launches window to confirm new point data
        '''
        self.locationConfirm = LocationWindow(lat, lon, self)
        self.locationConfirm.show()


    def setLocation(self, lat, lon, desc):
        '''
        Adds location to points list and passes list to Table class to update table data
        '''
        self.locationTracker.close()
        data = {
            'Latitude': lat,
            'Longitude': lon,
            'Date': QDateTime().currentDateTime().toString('MM-dd-yyyy hh:mm:ss ap'),
            'Description': desc
        }
        self.points.append(data)
        self.table.update(self.points)
        self.exportMenu.setEnabled(True)

    def exportToCSV(self):
        '''
        Export table data to csv file
        '''
        df = pd.DataFrame(self.points)
        df.to_csv(f'{QDate.currentDate().toString("MM-dd-yy")}_Report.csv')  

    def exportToJSON(self):
        '''
        Export table data to json file
        '''
        df = pd.DataFrame(self.points)
        df.to_json(f'{QDate.currentDate().toString("MM-dd-yy")}_Report.json')

    def exportToExcel(self):
        '''
        Export table data to excel file
        '''
        df = pd.DataFrame(self.points).set_index('Date')
        df.to_excel(f'{QDate.currentDate().toString("MM-dd-yy")}_Report.xlsx')

    def exportToHTML(self):
        '''
        Export table data to html file
        '''
        df = pd.DataFrame(self.points)
        df.to_html(f'{QDate.currentDate().toString("MM-dd-yy")}_Report.html')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())