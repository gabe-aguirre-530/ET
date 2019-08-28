import sys
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from geopy.distance import geodesic
from collections import namedtuple
import math

#Dependencies
#PyQt5: conda install -c anaconda pyqt 
#geopy: conda install -c conda-forge geopy

#Create namedtuple for readability to store point data
Point = namedtuple('Point', 'x y')

class Scale(QWidget):
    def __init__(self, dist_px, tracker):
        super(Scale, self).__init__()

        self.dist_px = dist_px
        self.scale = 1
        self.tracker = tracker

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
            self.tracker.setScale(pxPerUnit, units)        
            self.close()

    def cancel(self):
        '''
        Return to mouse tracker screen if cancel button is clicked
        '''
        self.close()

class Locator(QWidget):
    def __init__(self, lat, lon, tracker):
        super(Locator, self).__init__()
        self.lat = lat
        self.lon = lon
        self.tracker = tracker

        #self.setFixedSize(300, 100)
        self.setWindowTitle('Locator')
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
        Send scale and unit values entered by user back to mouse tracker
        screen when save button is clicked.
        '''
        #Get text values from each element
        lat = eval(self.latEdit.text())
        lon = eval(self.lonEdit.text())
        desc = self.descBox.toPlainText()
        
        #check values entered by user are correct
        if lat > -90 and lat < 90 and lon > -180 and lon < 180:
            self.tracker.setNewLocation(lat, lon, desc)
            self.close()

    def cancel(self):
        '''
        Return to mouse tracker screen if cancel button is clicked
        '''
        self.close()
    
class ReferencePoint(QWidget):
    def __init__(self, parent):
        super(ReferencePoint, self).__init__()
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

#Tracker class to handle mouse movement for locating point and setting scale
#Two modes: scale and locator
class Tracker(QWidget):
    
    def __init__(self, mode, parent, hidden=True, ref=None, scale=None, units=None):
        super(Tracker, self).__init__()

        if mode not in ['scale', 'locator']:
            raise ValueError(mode)

        self.ref = ref
        self.mode = mode
        self.parent = parent
        self.hidden = hidden
        self.scale = scale
        self.units = units

        self.zeroVariables()
           
        self.cursor = QtGui.QCursor()
        self.initUI()
        
        
    def initUI(self):
        '''
        Setup GUI elements of mouse tracker screen.
        '''      
        grid = QGridLayout()

        #Simplified label for scale mode
        if self.mode == 'scale':
            results = f'''
        dx_px: 0
        dy_px: 0
        Distance_px: 0
        '''

        #Label for locator mode
        if self.mode == 'locator':
            results = f'''
        Ref Point: {self.ref}
        dx_px: {self.dx}
        dy_px: {self.dy}
        Bearing: {self.bearing}
        Distance_px: {self.dist_px}
        Distance_{self.units}: {self.dist_km}
        New Location: {self.newLoc.x, self.newLoc.y}
        '''

        #Increase font size and set window dimensions
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label = QLabel(results, self)
        self.label.setFont(font)          
        grid.addWidget(self.label, 0, 0, Qt.AlignTop)
        self.setLayout(grid)

        self.setFixedSize(1080, 768)

        self.setWindowTitle(self.mode)
        self.show()
        
    def getCenter(self):
        '''
        Find the center point of the window by adding half the distance of
        the height and width to the absolute x, y location of the window.
        '''
        #Reference to geometry of screen and cursor
        geo = self.geometry()
        cur = self.cursor
        
        #Get x, y coords of the screen, left upper corner
        x_pos = geo.x()
        y_pos = geo.y()
            
        #Get width and height of screen distances from left upper corner
        width = geo.width()
        height = geo.height()
            
        #Find center point of screen
        x_center = x_pos + (width//2)
        y_center = y_pos + (height//2)
        
        return Point(x_center, y_center)
    
    def getCursorPos(self):
        '''
        Return the current position of the cursor relative to the upper
        left corner of the window.
        '''
        x = self.cursor.pos().x()
        y = self.cursor.pos().y()
        
        return Point(x, y)

    def getDX(self):
        '''
        Calculate distance from center in x direction
        '''
        center = self.getCenter()
        curPos = self.getCursorPos()

        return curPos.x - center.x

    def getDY(self):
        '''
        Calculate distance from center in y direction
        '''
        center = self.getCenter()
        curPos = self.getCursorPos()

        #reverse y for inverted y-axis
        return center.y - curPos.y

    def getDistance(self, dx, dy):
        '''
        Calculate straight line distance from point a to b using net distance
        in x and y direction

        Args:
            dx (float): total distance in pixels traveled in x direction
            dy (float): total distance in pixels traveled in y direction
        
        Returns:
            Total distance
        '''
        try:
            return round(math.sqrt(dx**2 + dy**2), 2)

        except:
            return 0

    def getBearing(self, dx, dy):
        '''
        Calculate the bearing of the mouse movement

        Args:
            dx (float): total distance in pixels traveled in x direction
            dy (float): total distance in pixels traveled in y direction

        Returns:
            bearing (float): bearing in degrees
        '''
        try:
            bearing = math.degrees(math.atan2(dy, dx))

        except Exception as e:
            print('Error: getBearing:', e.__class__.__name__)
            #do something to handle error
            return 1

        else:
            #shift bearing so 0 degrees is now grid north
            bearing = (360 + (90 - bearing)) % 360

            return round(bearing, 2)
    
    def convert(self, dist, scale):
        '''
        Convert distance in pixels to unit of measurement (km, mi, etc...)

        Args:
            dist (float): Euclidean distances from start to end point
            scale (int): scale to convert pixels to proper units

        Returns:
            convDist (float): converted mouse movement in correct unit of measurement
        '''
        try:
            convDist = dist / scale

        except Exception as e:
            print('Error: convert:', e.__class__.__name__)
            #do something to handle error
            return 1

        else:
            return round(convDist, 2)
    
    def newLocation(self, ref, dist, bearing):
        '''
        Computes the latitude and longitude using mouse movements distance
        and bearing from a reference point

        Args:
            ref (tuple): latitude and longitude of the reference point
            dist (float): converted euclidean distance of mouse movement
            bearing (float): bearing in degrees of mouse movement

        Returns:
            coords.latitude (float): latitude of new location
            coords.longitude(float): longitude of new location
        '''
        #kilometers
        if self.units == 'km':
            coords = geodesic(kilometers=dist).destination(ref, bearing)
        #miles    
        elif self.units == 'mi':
            coords = geodesic(miles=dist).destination(ref, bearing)
        #meters        
        elif self.units == 'm':
            coords = geodesic(meters=dist).destination(ref, bearing)
        #feet    
        elif self.units == 'ft':
            coords = geodesic(feet=dist).destination(ref, bearing)
    
        return Point(round(coords.latitude, 5), round(coords.longitude, 5))

    def launchScaleWindow(self):
        '''
        Launches window to confirm scale data after mouse has been released
        '''
        self.scaleWindow = Scale(self.dist_px, self)
        self.scaleWindow.show()

    def setScale(self, scale, units):
        '''
        Sends data to MainWindow to set scale data
        '''
        self.parent.setScale(scale, units)
        self.close()

    def launchLocatorWindow(self):
        '''
        Launches window to confirm lat/lon data of new point
        '''
        self.locatorWindow = Locator(self.newLoc.x, self.newLoc.y, self)
        self.locatorWindow.show()

    def setNewLocation(self, lat, lon, desc):
        '''
        Sends data to MainWindow to update points list
        '''
        self.parent.addLocation(lat, lon, desc)
        self.close()
    
    def zeroVariables(self):
        '''
        Zero out all instance variables after mouse has been released.
        '''
        self.dx = 0
        self.dy = 0
        self.dist_km = 0
        self.dist_px = 0
        self.bearing = 0
        self.newLoc = Point(0, 0)

    def updateForScaleMode(self):
        '''
        Tracks current x and y distance and updates label for scale mode
        '''
        geo = self.geometry()
        cur = self.cursor
        center = self.getCenter()
        
        #Get current x, y, and straight line distance from center
        dx_px = self.getDX()
        dy_px = self.getDY()
        self.dist_px = self.getDistance(self.dx + dx_px, self.dy + dy_px)
            
        #Check if cursor is within window boundaries
        #Only update dx, dy instance variables when border has been reached
        if not geo.contains(cur.pos()):
            self.dx += dx_px
            self.dy += dy_px
            cur.setPos(center.x, center.y)
        
        #Constantly update label while mouse is clicked and moving
        results = f'''
        dx_px: {self.dx + dx_px}
        dy_px: {self.dy + dy_px}
        Distance_px: {self.dist_px}
        '''
        self.label.setText(results)

    def updateForLocatorMode(self):
        '''
        Tracks current x and y distance and updates label for locator mode
        '''
        geo = self.geometry()
        cur = self.cursor
        center = self.getCenter()
        
        #Get current x, y, and straight line distance from center
        dx_px = self.getDX()
        dy_px = self.getDY()

        #Update bearing, distance in pixels, distance in units, and the new location
        self.bearing = self.getBearing(self.dx + dx_px, self.dy + dy_px)
        self.dist_px = self.getDistance(self.dx + dx_px, self.dy + dy_px)
        self.dist_km = self.convert(self.dist_px, self.scale)
        self.newLoc = self.newLocation(self.ref, self.dist_km, self.bearing)
            
        #Check if cursor is within window boundaries
        #Only update dx, dy instance variables when border has been reached
        if not geo.contains(cur.pos()):
            self.dx += dx_px
            self.dy += dy_px
            cur.setPos(center.x, center.y)
        
        #Constantly update label while mouse is clicked and moving
        results = f'''
        Ref Point: {self.ref}
        dx_px: {self.dx + dx_px}
        dy_px: {self.dy + dy_px}
        Bearing: {self.bearing}
        Distance_px: {round(self.dist_px, 2)}
        Distance_{self.units}: {self.dist_km}
        New Location: {self.newLoc.x, self.newLoc.y}
        '''
        self.label.setText(results)

        
    def mousePressEvent(self, e):
        '''
        When mouse is pressed cursor will be repositioned at the center
        of the window and tracking will start.
        '''
        center = self.getCenter()
        self.cursor.setPos(center.x, center.y)
                
        if self.hidden:
            QApplication.setOverrideCursor(Qt.BlankCursor)
        else:
            QApplication.setOverrideCursor(Qt.CrossCursor)
    
    def mouseReleaseEvent(self, e):
        '''
        When mouse is released cursor type will be reset or shown
        again if hidden.
        '''
        #restore cursor type and zero out variables
        QApplication.restoreOverrideCursor()

        #Call function to launch windown depending on scale or locator mode
        if self.mode == 'scale':
            self.launchScaleWindow()

        else:
            self.launchLocatorWindow()

        self.zeroVariables()
        
    def mouseMoveEvent(self, e):
        '''
        When mouse button is pressed and moving all fields will be actively updated.
        The current distance x, y, and total from the center will be added to the 
        overall distance to track current bearing, distance, and current location.
        '''
        if self.mode == 'scale':
            self.updateForScaleMode()

        else:
            self.updateForLocatorMode()