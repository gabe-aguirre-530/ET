import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime, QDate
import pandas as pd
import json

import Tracker
from Table import Table
from Windows import *

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
        self.fileMenu = menubar.addMenu('File')
        self.fileMenu.triggered.connect(self.checkPointsEmpty)

        self.menuNew = QAction("&New Project", self)
        self.menuNew.setShortcut("Ctrl+N")
        self.menuNew.setStatusTip('New Project')
        self.menuNew.triggered.connect(self.newProject)

        self.menuSave = QAction("&Save File", self)
        self.menuSave.setShortcut("Ctrl+S")
        self.menuSave.setStatusTip('Save File')
        self.menuSave.triggered.connect(self.saveFile)

        self.menuOpen = QAction("&Open File", self)
        self.menuOpen.setShortcut("Ctrl+O")
        self.menuOpen.setStatusTip('Open File')
        self.menuOpen.triggered.connect(self.openFile)

        self.menuExit = QAction("&Exit", self)
        self.menuExit.setShortcut("Ctrl+Q")
        self.menuExit.setStatusTip('Leave The App')
        self.menuExit.triggered.connect(self.closeApplication)
        
        self.menuExport = QMenu('Export', self)
        self.menuExport.setEnabled(False)
        
        self.exportCSV = QAction('CSV', self)
        self.menuExport.addAction(self.exportCSV)
        self.exportCSV.triggered.connect(self.exportToCSV)

        self.exportJSON = QAction('JSON', self)
        self.menuExport.addAction(self.exportJSON)
        self.exportJSON.triggered.connect(self.exportToJSON)

        self.exportExcel = QAction('Excel', self)
        self.menuExport.addAction(self.exportExcel)
        self.exportExcel.triggered.connect(self.exportToExcel)

        self.exportHTML = QAction('HTML', self)
        self.menuExport.addAction(self.exportHTML)
        self.exportHTML.triggered.connect(self.exportToHTML)

        self.fileMenu.addAction(self.menuNew)
        self.fileMenu.addAction(self.menuOpen)
        self.fileMenu.addAction(self.menuSave)
        self.fileMenu.addMenu(self.menuExport)
        self.fileMenu.addAction(self.menuExit)
        self.setCentralWidget(self.table)

        self.show()
        

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
        self.menuExport.setEnabled(True)

    def saveFile(self):
        '''
        Saves the project data in json format and writes to a file
        '''
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File')
        savestate = {
            'Reference': self.reference,
            'Scale': self.scale,
            'Units': self.units,
            'Points': self.points
        }

        if filename != '':
            with open(filename, 'w') as f:
                f.write(json.dumps(savestate, indent=2))

    def openFile(self):
        '''
        Opens project data from json file and updates table with new values
        '''
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File')

        if filename != '':
            try:
                with open(filename, 'r') as f:
                    data = json.loads(f.read())
            except:
                QMessageBox.critical(
                    self,
                    'File Not Found',
                    f'{filename} is not supported')
            else:
                self.reference = data['Reference']
                self.scale = data['Scale']
                self.units = data['Units']
                self.points = data['Points']

                self.table.update(self.points)
    
    def newProject(self):
        '''
        Create new project by clearing all instance variables
        '''
        self.scale = None
        self.reference = None
        self.units = None
        self.points = []

        self.table.update(self.points)

    def closeApplication(self):
        '''
        '''
        choice = QMessageBox.question(
            self, 
            'Exit Application',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No
        )

        if choice == QMessageBox.Yes:
            sys.exit()

    def checkPointsEmpty(self):
        '''
        Connect to file menu if points has data export option will be enabled
        '''
        if self.points:
            self.menuExport.setEnabled(True)
        else:
            self.menuExport.setEnabled(False)

    def exportToCSV(self):
        '''
        Export table data to csv file
        '''
        df = pd.DataFrame(self.points)
        
        try:
            df.to_csv(f'{QDate.currentDate().toString("MM-dd-yy")}_Report.csv', index=False)   
        except:
            self.fileCreatedAlert('CSV', True)	
        else:
            self.fileCreatedAlert('CSV')

    def exportToJSON(self):
        '''
        Export table data to json file
        '''
        json_data = json.dumps(self.points, indent=2)
        
        try:
            with open(f'{QDate.currentDate().toString("MM-dd-yy")}_Report.json', 'w+') as f:
                f.write(json_data)
        except:
            self.fileCreatedAlert('JSON', True)	
        else:
            self.fileCreatedAlert('JSON')

    def exportToExcel(self):
        '''
        Export table data to excel file
        '''
        df = pd.DataFrame(self.points)
        
        try:
            df.to_excel(f'{QDate.currentDate().toString("MM-dd-yy")}_Report.xlsx', index=False)
        except:
            self.fileCreatedAlert('Excel', True)
        else:
            self.fileCreatedAlert('Excel')

    def exportToHTML(self):
        '''
        Export table data to html file
        '''
        df = pd.DataFrame(self.points)
        
        try:
            df.to_html(f'{QDate.currentDate().toString("MM-dd-yy")}_Report.html', index=False)	
        except:
            self.fileCreatedAlert('HTML', True)
        else:
            self.fileCreatedAlert('HTML')
		
    def fileCreatedAlert(self, filetype, error=False):
        '''
        Display alert box to inform user export file was created
        '''
        if error:
            QMessageBox.critical(
                self,
                'Export File',
                f'{filetype} file failed to be created'
            )	
        else:
            QMessageBox.information(
                self,
                'Export File',
                f'{filetype} file was successfully created'
            )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())