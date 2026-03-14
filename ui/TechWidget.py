import math

from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget, QLabel

from ui.TechStats import TechStats


class TechWidget(QWidget):

    def __init__(self, tech_stats: TechStats, pos=QPoint(0,0), parent=None):
        from ui.TechTreeScene import TechTreeScene
        super().__init__(parent)

        self.CELL_SIZE = TechTreeScene.CELL_SIZE

        w, h = self.CELL_SIZE.width(), self.CELL_SIZE.height()
        self.setGeometry(int((pos.x()+0.1)*w),int((pos.y()+0.2)*h),int(w*0.8),int(h*0.6))

        self.tech_stats = tech_stats

        self.label = QLabel(self)
        self.label.setText(f' {tech_stats.Name}')
        self.label.setGeometry(0,0,self.width(),math.floor(self.height()/2))

        self.label_id = QLabel(self)
        self.label_id.setText(f' ID={str(tech_stats.ID)} T1={str(tech_stats.RequiredTech)} T2={str(tech_stats.RequiredTech2)}')
        self.label_id.setGeometry(0,math.floor(self.height()/2),self.width(),math.floor(self.height()/2))

        self.setSelected(False)


    def setPos(self, pos: QPoint):
        geometry = self.geometry()
        w, h = self.CELL_SIZE.width(), self.CELL_SIZE.height()
        self.setGeometry(int((pos.x()+0.1)*w), int((pos.y()+0.2)*h), geometry.width(), geometry.height())


    def setSelected(self, is_selected: bool):
        if is_selected:
            self.setStyleSheet("""QWidget {   color: black; background-color: rgb(255,255,255);  }""")
            self.label.setStyleSheet(f"""font-size: {math.floor(self.height()/3)}px; background-color: rgb(191,191,191) """)
            self.label_id.setStyleSheet(f"""font-size: {math.floor(self.height()/3.5)}px; background-color: rgba(0,0,0,0) """)
        else:
            self.setStyleSheet("""QWidget {   color: white; background-color: rgb(31,31,31);  }""")
            self.label.setStyleSheet(f"""font-size: {math.floor(self.height()/3)}px; background-color: rgb(63,63,63) """)
            self.label_id.setStyleSheet(f"""font-size: {math.floor(self.height()/4)}px; background-color: rgba(0,0,0,0) """)