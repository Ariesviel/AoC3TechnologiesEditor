from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QMainWindow, QGraphicsView

from ui.TechTreeScene import TechTreeScene


class TechTreeEditorWindow(QMainWindow):

    def __init__(self, file_path=None):
        super().__init__()
        self.setUI(file_path)


    def resizeEvent(self, event, /):
        self.view.setGeometry(0,0,self.width(),self.height())


    def setUI(self, file_path):
        screen = QGuiApplication.primaryScreen()
        self.setMinimumSize(
            int((600/1920)*screen.size().width()),
            int((400/1080)*screen.size().height())
        )
        self.resize(self.minimumSize()*2)

        self.scene = TechTreeScene(file_path)
        self.view = QGraphicsView(self.scene,self)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.view.setDragMode(QGraphicsView.NoDrag)
        self.view.centerOn(0,0)