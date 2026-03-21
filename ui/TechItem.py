from typing import Final, Optional

from PySide6.QtCore import QRectF, QSize, QPointF, QPoint
from PySide6.QtGui import QFont, QColor, QPen
from PySide6.QtWidgets import QGraphicsItem

from ui.TechTreeScene import TechTreeScene
CELL_SIZE = TechTreeScene.CELL_SIZE


class TechItem(QGraphicsItem):

    OFFSET: Final = min(CELL_SIZE.width(),CELL_SIZE.height())/5

    SIZE: Final[QSize] = QSize(
        CELL_SIZE.width()-OFFSET*2,
        CELL_SIZE.height()-OFFSET*2
    )

    SELECTED_BORDER_COLOR: Final[QColor] = QColor(239, 239, 239)
    PEN_SELECTED_BORDER_COLOR: Final[QPen] = QPen(SELECTED_BORDER_COLOR, OFFSET / 13.75)

    SELECTED_COLOR: Final[QColor] = QColor(223, 223, 223)
    SELECTED_FONT_COLOR: Final[QColor] = QColor(0, 0, 0)

    BORDER_COLOR: Final[QColor] = QColor(91, 91, 91)
    PEN_BORDER_COLOR: Final[QPen] = QPen(BORDER_COLOR, OFFSET / 13.75)

    COLOR: Final[QColor] = QColor(47, 47, 47)
    FONT_COLOR: Final[QColor] = QColor(255, 255, 255)

    def boundingRect(self): return QRectF(0,0, self.SIZE.width(), self.SIZE.height())

    def __init__(self,*,
        #/* Technology args/mods
        Name: str = "", MaintainTechnologyName: Optional[bool] = True, ImageID: int = 0,

        TreeColumn: int = 0, TreeRow: int = 0,

        RequiredTech: int = None, RequiredTech2: int = None,

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
        # Technology args/mods */
        ):
        #/* Assign technology args/mods
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
        # Assign technology args/mods */
        super().__init__()
        self.setPos(QPoint(TreeColumn, TreeRow))
        self.is_selected = False

    def set_selected(self, is_selected): self.is_selected = is_selected

    def setX(self, x):
        super().setX(x*CELL_SIZE.width()+self.OFFSET)
        self.TreeColumn = x

    def setY(self, y):
        super().setY(y*CELL_SIZE.height()+self.OFFSET)
        self.TreeRow = y

    def setPos(self, pos):
        self.setX(pos.x())
        self.setY(pos.y())

    def x(self): return super().x()-self.OFFSET

    def y(self): return super().y()-self.OFFSET

    def pos(self): return QPointF(self.x(), self.y())

    def ID(self): return self.scene().tech_items.index(self)

    def paint(self, painter, option, /, widget = ...):
        rect = self.boundingRect()

        #/* Change pen and brush for draw background
        if self.is_selected:
            painter.setPen(self.PEN_SELECTED_BORDER_COLOR)
            painter.setBrush(self.SELECTED_COLOR)
        else:
            painter.setPen(self.PEN_BORDER_COLOR)
            painter.setBrush(self.COLOR)
        # Change pen and brush for draw background */

        painter.drawRect(rect) # Draw background

        #/* Change pen and brush for draw background for name label
        if self.is_selected:
            painter.setBrush(self.SELECTED_BORDER_COLOR)
        else:
            painter.setBrush(self.BORDER_COLOR)
        # Change pen and brush for draw background for name label */

        painter.drawRect(rect.x(),rect.y(),rect.width(),rect.height()/3) # Draw background for name label

        #/* Change pen and brush for name label
        if self.is_selected:
            painter.setPen(self.SELECTED_FONT_COLOR)
            painter.setBrush(self.SELECTED_FONT_COLOR)
        else:
            painter.setPen(self.FONT_COLOR)
            painter.setBrush(self.FONT_COLOR)
        # Change pen and brush for name label */

        #/* Draw name
        painter.setFont(QFont('Arial',self.SIZE.height()/4.75))
        painter.drawText(
            QPoint(
                1*(self.scene().CELL_SIZE.width()/300),
                15*(self.scene().CELL_SIZE.height()/100)
            ), str(self.Name))
        # Draw name */

        #/* Draw ID
        painter.setFont(QFont('Arial',self.SIZE.height()/3))
        painter.drawText(
            QPoint(
                3*(self.scene().CELL_SIZE.width()/300),
                50*(self.scene().CELL_SIZE.height()/100)
            ), f"ID={self.ID()}")
        # Draw ID */