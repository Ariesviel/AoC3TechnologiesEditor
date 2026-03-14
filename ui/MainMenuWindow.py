from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QMainWindow, QPushButton, QFileDialog

from ui.TechTreeEditorWindow import TechTreeEditorWindow


class MainMenuWindow(QMainWindow):
    def __init__(self, screenSize: QSize):
        super().__init__()
        self.setWindowTitle('AoC3TechnologiesEditor')
        self.screenSize = screenSize
        self.setUI()


    def resizeEvent(self, event):
        width, height = event.size().toTuple()

        self.createNewTreeButton.setGeometry(
            int(width/2-width/3),
            int(2*height/7-height/8),
            int(width/1.5),
            int(height/4)
        )
        self.createNewTreeButton.setStyleSheet(
            f'font-size: {min(int(self.createNewTreeButton.height()*0.7), int(1.8*self.createNewTreeButton.width()/len(self.createNewTreeButton.text())))}px;'
        )

        self.openTreeButton.setGeometry(
            int(width/2-width/3),
            int(5*height/7-height/8),
            int(width/1.5),
            int(height/4)
        )
        self.openTreeButton.setStyleSheet(
            f'font-size: {min(int(self.openTreeButton.height()*0.7), int(1.8*self.openTreeButton.width()/len(self.openTreeButton.text())))}px;'
        )


    def openFile(self, file_path):
        self.techTreeEditorWindow = TechTreeEditorWindow(self.screenSize, file_path)
        self.techTreeEditorWindow.show()


    def openFileDialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose file",
            "",
            "Все файлы (*.*)"
        )
        self.openFile(file_path)


    def setUI(self):
        self.setMinimumSize(
            int((300/1920)*self.screenSize.width()),
            int((400/1080)*self.screenSize.height())
        )
        self.resize(self.minimumSize())

        self.setMaximumSize(self.screenSize)

        self.createNewTreeButton = QPushButton(self)
        self.createNewTreeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.createNewTreeButton.setText('New Technologies Tree')

        self.openTreeButton = QPushButton(self)
        self.openTreeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.openTreeButton.setText('Open Technologies Tree')
        self.openTreeButton.clicked.connect(self.openFileDialog)