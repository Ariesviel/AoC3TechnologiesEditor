from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QMainWindow

from ui.TechTreeScene import TechTreeScene
from ui.TechTreeView import TechTreeView


class TechTreeEditorWindow(QMainWindow):

    def __init__(self, file_path=None):
        super().__init__()
        self.set_ui(file_path)


    def resizeEvent(self, event, /):
        self.view.setGeometry(0,32,self.width(),self.height()-32)


    def set_ui(self, file_path):
        screen = QGuiApplication.primaryScreen()
        self.setMinimumSize(
            int((800/1920)*screen.size().width()),
            int((533/1080)*screen.size().height())
        )
        self.resize(self.minimumSize()*1.5)

        self.scene = TechTreeScene(file_path)
        self.view = TechTreeView(self.scene,self)
        self.view.centerOn(0,0)