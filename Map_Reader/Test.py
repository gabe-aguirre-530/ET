from MainWindow import MainWindow
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import time
import sys
import pytest

@pytest.fixture
def window():
    window = MainWindow()
    return window

def test_reference_point1(qtbot, window):
    '''
    Test if setting reference point data is correctly passed
    and stored in reference tuple from main window when save
    button is pressed
    '''
    qtbot.addWidget(window)

    qtbot.mouseClick(window.table.addRefButton, QtCore.Qt.LeftButton)
    rw = window.refWindow
    
    qtbot.keyClicks(rw.latEdit, '37.343')
    qtbot.keyClicks(rw.lonEdit, '121.343')
    qtbot.mouseClick(rw.saveButton, QtCore.Qt.LeftButton)

    assert window.reference[0] == 37.343
    assert window.reference[1] == 121.343

def test_reference_point2(qtbot, window):
    '''
    Test if save button in referene window is disabled when only
    lat input is entered
    '''
    qtbot.addWidget(window)

    qtbot.mouseClick(window.table.addRefButton, QtCore.Qt.LeftButton)
    rw = window.refWindow
    
    qtbot.keyClicks(rw.latEdit, '70.123')
    qtbot.mouseClick(rw.saveButton, QtCore.Qt.LeftButton)

    assert rw.saveButton.isEnabled() == False

def test_reference_point3(qtbot, window):
    '''
    Test if save button in referene window is disabled when only
    lon input is entered
    '''
    qtbot.addWidget(window)

    qtbot.mouseClick(window.table.addRefButton, QtCore.Qt.LeftButton)
    rw = window.refWindow
    
    qtbot.keyClicks(rw.lonEdit, '121.1234')
    qtbot.mouseClick(rw.saveButton, QtCore.Qt.LeftButton)

    assert rw.saveButton.isEnabled() == False

def test_reference_point4(qtbot, window):
    '''
    Test if reference point data is not stored when erroneous data
    is entered to lat and lon fields
    '''
    qtbot.addWidget(window)

    qtbot.mouseClick(window.table.addRefButton, QtCore.Qt.LeftButton)
    rw = window.refWindow
    
    qtbot.keyClicks(rw.latEdit, '91.343')
    qtbot.keyClicks(rw.lonEdit, '-7000.343')
    qtbot.mouseClick(rw.saveButton, QtCore.Qt.LeftButton)

    assert window.reference == None

def test_reference_point5(qtbot, window):
    '''
    Test that no information is saved in main window reference
    tuple when cancel is pressed
    '''
    qtbot.addWidget(window)

    qtbot.mouseClick(window.table.addRefButton, QtCore.Qt.LeftButton)
    rw = window.refWindow
        
    qtbot.keyClicks(rw.latEdit, '37.343')    
    qtbot.keyClicks(rw.lonEdit, '121.343')
    qtbot.mouseClick(rw.cancelButton, QtCore.Qt.LeftButton)

    assert window.reference == None
    