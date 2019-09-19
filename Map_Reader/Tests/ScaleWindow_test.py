from Map_Reader.Windows import ScaleWindow
from PyQt5 import QtCore
import pytest

@pytest.fixture
def window():
    window = ScaleWindow(100)
    return window

def test_1(qtbot, window):
    qtbot.addWidget(window)
    
    assert window.pixelEdit.text() == '100'