from typing import Final, Optional

from PySide6.QtCore import QRectF, Qt, QSize, QPointF
from PySide6.QtGui import QFont, QColor, QBrush, QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsSimpleTextItem

from ui.TechTreeScene import TechTreeScene
CELL_SIZE = TechTreeScene.CELL_SIZE


class TechItem(QGraphicsItem):

    OFFSET: Final = min(CELL_SIZE.width(),CELL_SIZE.height())/5

    SIZE: Final[QSize] = QSize(
        CELL_SIZE.width()-OFFSET*2,
        CELL_SIZE.height()-OFFSET*2
    )

    def boundingRect(self): return QRectF(0,0, self.SIZE.width(), self.SIZE.height())

    def __init__(self,*,
                 # ID: int=None,
                 Name: str = "", MaintainTechnologyName: Optional[bool] = True, ImageID: int = 0,

                 TreeColumn: int = 0, TreeRow: int = 0,

                 RequiredTech: int = -1, RequiredTech2: int = -1,

                 UnlocksNukes: bool = False,
                 UnlocksAccessToTheSea: bool = False,

                 MaximumLevelOfCapitalCity: Optional[int] = None,
                 MaximumLevelOfTheMilitaryAcademy: Optional[int] = None,
                 MaximumLevelOfTheMilitaryAcademyForGenerals: Optional[int] = None,

                 BattleWidth: Optional[int] = None,
                 UnitsAttack: Optional[int] = None, UnitsDefense: Optional[int] = None,
                 GeneralAttack: Optional[int] = None, GeneralDefense: Optional[int] = None,
                 MaxMorale: Optional[int] = None, Discipline: Optional[int] = None,

                 Legacy: Optional[int] = None,

                 ResearchCost: int = 0,
                 Repeatable: bool = False,
                 AI: int = 5,
                 **kwargs
        ):
        print(kwargs)
        self.TreeColumn, self.TreeRow = TreeColumn, TreeRow
        self.Name, self.MaintainTechnologyName, self.ImageID = Name, MaintainTechnologyName, ImageID
        self.RequiredTech, self.RequiredTech2 = RequiredTech, RequiredTech2

        self.UnlocksNukes = UnlocksNukes
        self.UnlocksAccessToTheSea = UnlocksAccessToTheSea

        self.MaximumLevelOfCapitalCity = MaximumLevelOfCapitalCity
        self.MaximumLevelOfTheMilitaryAcademy = MaximumLevelOfTheMilitaryAcademy
        self.MaximumLevelOfTheMilitaryAcademyForGenerals = MaximumLevelOfTheMilitaryAcademyForGenerals

        self.BattleWidth = BattleWidth
        self.UnitsAttack, self.UnitsDefense = UnitsAttack, UnitsDefense
        self.GeneralAttack, self.GeneralDefense = GeneralAttack, GeneralDefense
        self.MaxMorale, self.Discipline = MaxMorale, Discipline

        self.Legacy = Legacy

        self.ResearchCost = ResearchCost

        self.Repeatable = Repeatable
        self.AI = AI
        super().__init__()
        self.setPos(TreeColumn, TreeRow)
        self.setUI()

    def setX(self, x):
        super().setX(x*CELL_SIZE.width()+self.OFFSET)
        self.TreeColumn = x

    def setY(self, y):
        super().setY(y*CELL_SIZE.height()+self.OFFSET)
        self.TreeRow = y

    def setPos(self, pos):
        self.setX(pos.x())
        self.setY(pos.y())

    def setPos(self, x, y):
        self.setX(x)
        self.setY(y)

    def x(self): return super().x()-self.OFFSET

    def y(self): return super().y()-self.OFFSET

    def pos(self): return QPointF(self.x(), self.y())

    def ID(self): return self.scene().techItems.index(self)

    def setUI(self):
        self.nameLabel = QGraphicsSimpleTextItem(self.Name, self)
        self.nameLabel.setBrush(QBrush(Qt.white))
        self.nameLabel.setFont(QFont('Arial',self.SIZE.height()/4.75))
        self.nameLabel.setPos(self.OFFSET*0.1,self.OFFSET*0.0375)
        self.IDLabel = QGraphicsSimpleTextItem(f"", self)
        self.IDLabel.setBrush(QBrush(Qt.white))
        self.IDLabel.setFont(QFont('Arial',self.SIZE.height()/3))
        self.IDLabel.setPos(self.OFFSET*0.15,self.SIZE.height()/3+self.OFFSET*0.3)


    def paint(self, painter, option, /, widget = ...):
        self.nameLabel.setText(str(self.Name))
        self.IDLabel.setText("ID="+str(self.ID()))
        rect = self.boundingRect()

        painter.setPen(QPen(QColor(91,91,91),self.OFFSET/13.75))
        painter.setBrush(QColor(47,47,47))

        painter.drawRect(rect)

        painter.setBrush(QColor(91,91,91))

        painter.drawRect(rect.x(),rect.y(),rect.width(),rect.height()/3)