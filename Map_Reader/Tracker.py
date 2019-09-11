import sys
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QGridLayout, QLabel, QApplication, QDialog
from PyQt5.QtGui import QCursor, QFont
from geopy.distance import geodesic
from collections import namedtuple
import math

#Dependencies
#PyQt5: conda install -c anaconda pyqt 
#geopy: conda install -c conda-forge geopy

#Create namedtuple for readability to store point data
Point = namedtuple('Point', 'x y')

#Tracker class to handle mouse movement for locating point and setting scale
#Two modes: scale and location
class Tracker(QDialog):
    
    def __init__(self, mode, parent, hidden=True, ref=None, scale=None, units=None):
        super(Tracker, self).__init__(parent)

        if mode not in ['scale', 'location']:
            raise ValueError(mode)

        self.ref = ref
        self.mode = mode
        self.hidden = hidden
        self.scale = scale
        self.units = units

        self.zeroVariables()
           
        self.cursor = QCursor()
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

        #Label for location mode
        if self.mode == 'location':
            results = f'''
        Ref Point: {self.ref}
        dx_px: {self.dx}
        dy_px: {self.dy}
        Bearing: {self.bearing}
        Distance_px: {self.dist_px}
        Distance_{self.units}: {self.dist}
        New Location: {self.newLoc.x, self.newLoc.y}
        '''

        #Increase font size and set window dimensions
        font = QFont()
        font.setPointSize(14)
        self.label = QLabel(results, self)
        self.label.setFont(font)          
        grid.addWidget(self.label, 0, 0, Qt.AlignTop)
        self.setLayout(grid)

        self.setFixedSize(1080, 768)

        self.setWindowTitle(self.mode)
        self.showFullScreen()
    
        
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
    
    def zeroVariables(self):
        '''
        Zero out all instance variables after mouse has been released.
        '''
        self.dx = 0
        self.dy = 0
        self.dist = 0
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

    def updateForLocationMode(self):
        '''
        Tracks current x and y distance and updates label for location mode
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
        self.dist = self.convert(self.dist_px, self.scale)
        self.newLoc = self.newLocation(self.ref, self.dist, self.bearing)
            
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
        Distance_{self.units}: {self.dist}
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

        #Call function to launch windown depending on scale or location mode
        if self.mode == 'scale':
            self.parent().confirmScale(self.dist_px)
        else:
            self.parent().confirmLocation(self.newLoc.x, self.newLoc.y, self.dist, self.bearing, self.units)

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
            self.updateForLocationMode()