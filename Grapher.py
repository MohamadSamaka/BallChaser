from PyQt5 import QtWidgets as QW
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QMainWindow

class ScrollableWindow(QMainWindow):
    def __init__(self, fig):
        self.qapp = QW.QApplication([])

        QW.QMainWindow.__init__(self)
        self.widget = QW.QWidget()
        self.setCentralWidget(self.widget)
        titleBarHeight = self.style().pixelMetric(
            QW.QStyle.PM_TitleBarHeight,
            QW.QStyleOptionTitleBar(),
            self
        )
        geometry = self.qapp.desktop().availableGeometry()
        geometry.setHeight(geometry.height() - (titleBarHeight*2))
        self.setGeometry(geometry)
        self.widget.setLayout(QW.QVBoxLayout())
        self.widget.layout().setContentsMargins(0,0,0,0)
        self.widget.layout().setSpacing(0)

        self.fig = fig
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.scroll = QW.QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)

        self.nav = NavigationToolbar(self.canvas, self.widget)
        self.widget.layout().addWidget(self.nav)
        self.widget.layout().addWidget(self.scroll)
        self.showMaximized()
        exit(self.qapp.exec_()) 