import os

from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

import json

from MainWindow import MainWindow
from NewProjectWizard import NewProjectWizard

class StarterWindow(QDialog):
    def __init__(self):
        super(StarterWindow, self).__init__()
        self.setFixedSize(300, 100)
        self.setWindowTitle('Welcome')
        self.mw = None
        self.newProjectWizard = None

        #Create main projects directory
        if not os.path.exists('./Projects'):
            os.mkdir('./Projects')
        
        self.initUI()

    def initUI(self):
        '''
        Setup GUI elements of scale window
        '''
        mainLayout = QVBoxLayout()

        #horizontal layout containing new and open buttons
        hLayout = QHBoxLayout()
        self.projectTable = QTableView()

        self.newButton = QPushButton('New')
        self.newButton.clicked.connect(self.new)

        self.openButton = QPushButton('Open')
        self.openButton.clicked.connect(self.open)

        self.aboutButton = QPushButton('About')
        
        mainLayout.addWidget(self.projectTable)
        hLayout.addWidget(self.newButton)
        hLayout.addWidget(self.openButton)
        hLayout.addWidget(self.aboutButton)

        mainLayout.addLayout(hLayout)
    
        self.setLayout(mainLayout)

        self.show()

    def new(self):
        '''
        Send reference point back to main window to be stored
        '''
        self.newProjectWizard = NewProjectWizard(self)
        self.hide()
        

    def createProject(self, projectName, refPoint):
        '''
        Creates a new project and launch main window
        '''
        #Need to close mainwindow if new project was selected from that screen

        self.newProjectWizard.close()

        if self.mw:
            self.mw.close()

        createdDate = QDateTime().currentDateTime().toString('MM-dd-yyyy hh:mm:ss ap')

        #Creates project name directory and Reports subdirectory
        try:
            os.makedirs(f'./Projects/{projectName}/Reports')

        except FileExistsError:
            msg = f'{projectName} already exists'
            QMessageBox.critical(
                    self,
                    'Error Creating Project',
                    msg)

            self.show()
        
        #Create project_data.json file with new data and start main window
        else:
            defaultData = {
            'ProjectName': projectName,
            'Created': createdDate,
            'LastAccessed': createdDate,
            'Reference': refPoint,
            'Scale': 0,
            'Units': '',
            'Points': []
            }

            with open(f'./Projects/{projectName}/project_data.json', 'w+') as f:
                f.write(json.dumps(defaultData, indent=2))

            self.mw = MainWindow(
                projectName, 
                reference=refPoint, 
                createdDate=createdDate, 
                parent=self)
        
    def open(self):
        '''
        Open an existing project and launch main window
        '''
        self.hide()

        filename = None
        fileDialog = QFileDialog(self, 'Projects', './Projects')
        fileDialog.setFileMode(QFileDialog.DirectoryOnly)
        if fileDialog.exec_() == QDialog.Accepted:
            filename = fileDialog.selectedFiles()[0]
        
        #If a valid path is returned from file dialog screen
        if filename:
            #Check if json data file is in selected folder
            if os.path.exists(f'{filename}/project_data.json'):
                #close old project and open given project name
                if self.mw:
                    self.mw.close()
                self.mw = MainWindow(filename, self, openExisting=True)

            #alert for invalid project and return to main window or starter screen
            else:
                QMessageBox.critical(
                    self,
                    'Invalid Project',
                    f'{filename} is an invalid project')
                self.show()
        
        #If cancel is pressed from filedialog main starter screen should be reopened
        else:
            if not self.mw:
                self.show()

            #Bug causes complete exit when pressing cancel from filedialog when opened from MainWindow
            #if this screen is shown and hidden it wont exit completely out of application
            else:
                self.show()
                self.hide()

    def starterScreen(self, closeMW=False):
        '''
        Display starter page if hidden
        '''
        if closeMW:
            self.mw.close()

        if self.newProjectWizard:
            self.newProjectWizard.close()

        self.show()

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = StarterWindow()
    sys.exit(app.exec_())