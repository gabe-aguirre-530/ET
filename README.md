# Map Reader

By: Evan Brittain, 

**[Description](#Description)**

**[Dependencies](#Overview)**

**[Demo](#Demo)**

**[Overview](#Overview)**
* [Starter.py](#Starter.py)
* [NewProjectWizard.py](#NewProjectWizard.py)
* [MainWindow.py](#MainWindow.py)
* [Tracker.py](#Tracker.py)
* [Table.py](#Table.py)
* [Windows.py](#Windows.py)
* [MouseController.py](#MouseController.py)

**[Program Flow](#Program-Flow)**
* [Creating Projects](#Projects)
* [Locating Points](#Points) 

**[Structures](#Structures)**
* [Points](#Points)
* [Project Data](#Data) 

## Description

Map Reader is a tool that allows users to locate the coordinates of points on a map by tracing from a reference point with their mouse.

## Dependencies

	PyQt5: conda install -c anaconda pyqt
	geopy: conda install -c conda-forge geopy
	pytest-qt: conda install -c conda-forge pytest-qt

## Demo
![Demo](https://media.giphy.com/media/RJaUQoO9vMruZEolA2/giphy.gif)
## Overview

### Starter.py
**StarterWindow (QDialog):** This is the top level class that is responsible for creating new projects, opening existing projects, and hiding and displaying the correct windows. When this class is instantiated it creates a directory (./Projects/) if one doesn't already exist. This directory contatins all the project folders created by the user. If the 'New' button is clicked it will instantiate the NewProjectWizard class which will walk the user through creation of a new project.
		
	Creation of a new project includes:
	creating the project directory (./Projects/{Project_Name}/)
	creating reports folder used for storing exported data (./Projects/{Project_Name}/Reports/)
	creating JSON file used for storing all project data (./Projects/{Project_Name}/project_data.json).
		
When the user successfully creates and new project the reference point and project name entered will be used to launch an instance of MainWindow.
		
If the user clicks the 'Open' button the selected folder name (project name) will be used to create an instance of MainWindow and the openExisting flag in the MainWindow constructor will be set toTrue.
		
### NewProjectWizard.py

**NewProjectWizard (QWizard):** This class is only responsible for setting up the three pages in the new project wizard. The three pages include intro, data (created in it's own class: WizardDataPage), and conclusion. It's created with an instance of the parent window (StarterWindow) and passes all entered data (ref. point, project name) back to the parent class.
		
**WizardDataPage (QWizardPage):** This class is one of the pages in NewProjectWizard and is used to collect all project data entered by the user. This includes ensuring the project name entered is a valid windows folder name and latitude and longitude values are between (-90, 90) and (-180, 180).

### MainWindow.py

**MainWindow (QMainWindow):** This is the central point of the program where the user is able to enter a new reference point, trace the scale, locate a point, export data, and view the collected data in a table. Every window launched from this screen is a child of the MainWindow and uses MainWindow to pass all data back  and forth. The class is instantiated by passing a reference to it's parent (StarterWindow) and project name. It can also be created using the openExisting flag (False by default) which reads  data from (./Projects/{Project_Name}/project_data.json) and uses the data to set instance variables (scale, reference, units, points, createdDate, ...) and populate the table. The filemenu and central widget (Table) are defined and created in the constructor. Submenus are created within the filemenu to save, open, close, exit, export, and create new project. Each submenu is connected to a function which will be activated when clicked. Exporting data is done by creating a pandas dataframe with the self.points instance variable then calling the pandas function to export as HTML, JSON, CSV, or Excel.

### Tracker.py

**Tracker (QDialog):** This class is responsible for tracking the distance travelled by the mouse. Tracker is instantiated by passing an instance of it's parent (MainWindow) and selecting a mode. The two modes are scale and location which tell it whether the user is tracing the scale or tracing from the reference point to a location.
		
	Scale mode:
		Scale mode only tracks the dx, dy, and straight line distance of the mouse. It contains a simpler
		label to show the current distance travelled in each direction.

	Location mode:
		Location mode uses the reference point, scale, and units set in the constructor to find the
		bearing, distance in given units, and new location (lat, lon). Location mode also contains a more 
		in depth label to show how data is being changed while the user traces.
	
**Mouse Tracing:**
1. The center point of the window is found
2. The user clicks the mouse and the cursor is repositioned to the center point
3. Global dx, dy and local dx, dy values are set to 0
4. User traces in any direction while holding down left mouse button
5. local dx and dy values are contantly being tracked from the center point
6. User hits edge of screen
	```python 
	if  any(x in (cur.pos().x(), cur.pos().y()) for x in [0, geo.width()-1, geo.height()-1])
	```
7. Global dx, dy values are updated with local dx, dy values
	```python
	self.dx += dx_px
	self.dy += dy_px
	```
8. Cursor is repositioned to center of screen
9. local dx, dy values are set to 0
10. User released mouse button
11. Global dx, dy values are updated with local dx, dy values
12. Straight line distance is found
	```python
	self.dist_px =  self.getDistance(self.dx + dx_px, self.dy + dy_px)
	return  round(math.sqrt(dx**2  + dy**2), 4)
	```

**Locating New Point:**
1. User traces (see above)
2. Bearing is found with global dx, dy values
	```python 
	bearing = math.degrees(math.atan2(dy, dx))
	```
3. Bearing is shifted to grid north
	```python
	bearing = (360  + (90  - bearing)) %  360
	```
4. Distance is found with global dx, dy
5. New location is computed with bearing, distance, and reference point
	```python
	coords = geodesic(kilometers=dist).destination(ref, bearing)
	```
		
When the mouse is released all data will be passed back to the parent (MainWindow).

### Table.py

**Table (QWidget):** This class is only responsible for laying out the UI elements of the parent's (MainWindow) central widget and updating the table . It creates the main table and buttons (add reference, set scale, locate point) and connects each to the approriate function in the parent's class. It updates the table with self.points passed from the parent.

### Windows.py

**ScaleWindow (QDialog):** ScaleWindow is created to confirm the data traced by Tracker. It will be displayed when the user releases the mouse from tracing. The field is populated with the pixel distance tracked and the user needs to set the actual distance and units (km, mi, ft, m). When the data is confirmed it will be passed back to the parent (MainWindow).
		
**ReferenceWindow (QDialog):** ReferenceWindow is used to enter the lat, lon of the reference point. These values will be initially set by the NewProjectWizard but can be reset at anytime from the MainWindow. The user will enter the lat, lon and press save. The data will then be passed back to the parent (MainWindow).
			
**LocationWindow (QDialog):** LocationWindow is created when the user has finished tracing to a new location in Tracker. The window will be displayed with fields already populated and the user will confirm each and add a description (optional). When the user clicks save the confirmed data (lat, lon, bearing, distance, description) will be passed back to the parent (MainWindow)

### MouseController.py

**MouseController:** This class is only used to make system calls to the OS to modify mouse settings. The mouse settings it changes are speed and acceleration which are only manipulated when the user is actively tracing
					
## Program Flow

### Creating Projects:
1. User clicks 'New' from Starter
2. Starter creates instance of NewProjectWizard
3. User enters reference point and project name in data page of NewProjectWizard
4. Data is passed back to Starter
5. Directories, subdirectories, and project data file is created
6. Starter launches instance of MainWindow using project name and reference point data
7. Starter is hidden

### Finding Points:
1. User clicks 'Add Reference Point' button
2. MainWindow creates instance of ReferenceWindow to enter and confirm data
3. Data is confirmed from ReferenceWindow and passed back to MainWindow
4. User clicks 'Set Scale' button
5. MainWindow launches instance of Tracker to trace scale
6. Tracker passes data back to MainWindow when mouse is released
7. MainWindow creates instance of ScaleWindow to confirm traced data
8. Data is confirmed from ScaleWindow and passed back to MainWindow
9. User clicks 'Locate Point' button
10. MainWindow creates instance of Tracker to trace to new point
11. Data is passed back to MainWindow when mouse is released
12. MainWindow creates instance of LocationWindow to confirm new location, bearing, ...
13. Data is confirmed and passed back to MainWindow
14. Project data is updated and saved in project_data.json
15. Table is updated with new point

## Structures
		
### Point Data:
```python
self.points = [
	{
	'Latitude': float,
	'Longitude': float,
	'Date': QDateTime(str),
	'Description': str,
	'Distance': float,
	'Bearing': float,
	'Units': str,
	'ReferencePoint': tuple,
	'Scale': float
	}, ...
]
```

### Project Data:
```python
data = {
	'ProjectName': str,
	'Created': QDateTime(str),
	'LastAccessed': QDateTime(str),
	'Reference': tuple,
	'Scale': float,
	'Units': str,
	'Points': list
}
```
