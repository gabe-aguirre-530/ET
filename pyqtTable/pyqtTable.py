from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
        QTime)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
        QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
        QWidget)


PID, LAT, LON, DESC, DATE = range(5)

# Work around the fact that QSortFilterProxyModel always filters datetime
# values in QtCore.Qt.ISODate format, but the tree views display using
# QtCore.Qt.DefaultLocaleShortDate format.
class SortFilterProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, sourceRow, sourceParent):
        # Do we filter for the date column?
        if self.filterKeyColumn() == DATE:
            # Fetch datetime value.
            index = self.sourceModel().index(sourceRow, DATE, sourceParent)
            data = self.sourceModel().data(index)

            # Return, if regExp match in displayed format.
            return (self.filterRegExp().indexIn(data.toString(Qt.DefaultLocaleShortDate)) >= 0)

        # Not our business.
        return super(SortFilterProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.proxyModel = SortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)

        self.proxyGroupBox = QGroupBox("Points")

        self.proxyView = QTreeView()
        self.proxyView.setRootIsDecorated(False)
        self.proxyView.setAlternatingRowColors(True)
        self.proxyView.setModel(self.proxyModel)
        self.proxyView.setSortingEnabled(True)

        self.filterPatternLineEdit = QLineEdit()
        self.filterPatternLabel = QLabel("Search:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)

        self.filterPatternLineEdit.textChanged.connect(self.filterRegExpChanged)

        proxyLayout = QGridLayout()
        proxyLayout.addWidget(self.proxyView, 0, 0, 1, 3)
        proxyLayout.addWidget(self.filterPatternLabel, 1, 0)
        proxyLayout.addWidget(self.filterPatternLineEdit, 1, 1, 1, 2)
        self.proxyGroupBox.setLayout(proxyLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.proxyGroupBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Main Screen")
        self.resize(550, 400)

        self.proxyView.sortByColumn(PID, Qt.AscendingOrder)

    def setSourceModel(self, model):
        self.proxyModel.setSourceModel(model)

    def filterRegExpChanged(self):
        regExp = QRegExp(self.filterPatternLineEdit.text())
        self.proxyModel.setFilterRegExp(regExp)



def addPoint(model, pid, data):
    model.insertRow(0)
    model.setData(model.index(0, PID), pid)
    model.setData(model.index(0, LAT), data['lat'])
    model.setData(model.index(0, LON), data['lon'])
    model.setData(model.index(0, DESC), data['desc'])
    model.setData(model.index(0, DATE), data['date'])

def createMailModel(parent):
    model = QStandardItemModel(0, 5, parent)

    model.setHeaderData(PID, Qt.Horizontal, "Point ID")
    model.setHeaderData(LAT, Qt.Horizontal, "Latitude")
    model.setHeaderData(LON, Qt.Horizontal, "Longitude")
    model.setHeaderData(DESC, Qt.Horizontal, "Description")
    model.setHeaderData(DATE, Qt.Horizontal, "Date")

    data_dic = {
    	'001': {'lat': '32.806671', 'lon': '-86.791130', 'desc': 'Alabama', 
    		'date': QDateTime(QDate(2006, 12, 31), QTime(17, 3))},
    	'002': {'lat': '61.370716', 'lon': '-152.404419', 'desc': 'Alaska', 
    		'date': QDateTime(QDate(2006, 12, 31), QTime(17, 3))},
    	'003': {'lat': '33.729759', 'lon': '-111.431221', 'desc': 'Arizona', 
    		'date': QDateTime(QDate(2006, 12, 31), QTime(17, 3))}
    }

    for k,v in data_dic.items():
    	addPoint(model, k, v)

    return model


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.setSourceModel(createMailModel(window))
    window.show()
    sys.exit(app.exec_())