import math

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QLabel


class TechTreeEditorWindow(QMainWindow):
    def __init__(self, screenSize: QSize, file=None):
        super().__init__()
        self.screenSize = screenSize
        self.setUI(file)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = self.size()
        self.coordLabel.setGeometry(0,0,size.width(),math.ceil(size.width()/25))
        self.techTreeView.setGeometry(0,math.ceil(size.height()/25),size.width(),size.height()-math.ceil(size.height()/25))


    def setUI(self, file=None):
        self.setMinimumSize(
            int(0.5*self.screenSize.width()),
            int(0.5*self.screenSize.height())
        )
        self.resize(self.minimumSize())

        self.coordLabel = QLabel(self)

        from ui.TechTreeScene import TechTreeScene
        self.scene = TechTreeScene(file)

        from ui.TechTreeView import TechTreeView
        self.techTreeView = TechTreeView(self.scene, self)
        self.techTreeView.setGeometry(0,0,100,100)