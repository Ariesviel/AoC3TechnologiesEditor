from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QMainWindow, QPushButton, QInputDialog, QFileDialog

from ui.TechTreeScene import TechTreeScene
from ui.TechTreeView import TechTreeView


class TechTreeEditorWindow(QMainWindow):

    def __init__(self, file_path=None):
        super().__init__()
        self.set_ui(file_path)


    def resizeEvent(self, event, /):
        screen = QGuiApplication.primaryScreen()
        self.view.setGeometry(0,int(48/1920*screen.size().height()),self.width(),int(self.height()-48/1920*screen.size().height()))
        self.saveButton.setStyleSheet(f"font-size: {int(40/1920*screen.size().height())}")
        self.saveButton.setGeometry(0,0,int(40/1920*screen.size().height())*3,int(48/1920*screen.size().height()))


    def set_ui(self, file_path):
        screen = QGuiApplication.primaryScreen()
        self.setMinimumSize(
            int((800/1920)*screen.size().width()),
            int((533/1080)*screen.size().height())
        )
        self.resize(self.minimumSize()*1.5)

        self.saveButton = QPushButton("Export", self)
        self.saveButton.clicked.connect(self.export_techs)
        self.scene = TechTreeScene(file_path)
        self.view = TechTreeView(self.scene,self)
        self.view.centerOn(0,0)


    def export_techs(self):
        directory = QFileDialog.getExistingDirectory(self)
        if len(directory) > 0:
            with open(directory+"/Techs.json", "w", encoding="utf-8") as file:
                file.write('{\n')
                file.write('	Technology:\n')
                file.write('	[\n')
                file.write(self.view.export())
                file.write('	],\n')
                file.write('	Age_of_History: Technology\n')
                file.write('}')