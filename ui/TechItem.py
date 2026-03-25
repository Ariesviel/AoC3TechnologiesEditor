from typing import Final, Optional, ClassVar

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

    MODS: ClassVar[Final[tuple]] = (
        "ID","Name", "MaintainTechnologyName", "ImageID", "TreeColumn", "TreeRow", "RequiredTech", "RequiredTech2",
        "UnlocksNukes", "UnlocksAccessToTheSea",
        "MaximumLevelOfCapitalCity", "MaximumLevelOfTheMilitaryAcademy",
        "MaximumLevelOfTheMilitaryAcademyForGenerals",
        "BattleWidth", "UnitsAttack", "UnitsDefense",
        "GeneralAttack", "GeneralDefense", "MaxMorale", "Discipline",
        "Legacy", "ResearchCost", "Repeatable", "AI"
    )
    REQUIRED_MODS: ClassVar[Final[dict]] = {
        "ID": int,"Name": str, "ImageID": int, "TreeColumn": int, "TreeRow": int, "RequiredTech": int, "RequiredTech2": int, "ResearchCost": int, "Repeatable": bool, "AI": int
    }
    OPTIONAL_MODS: ClassVar[Final[dict]] = {
        "MaintainTechnologyName": True,
        "UnlocksNukes": False, "UnlocksAccessToTheSea": False,
        "MaximumLevelOfCapitalCity": 0, "MaximumLevelOfTheMilitaryAcademy": 0,
        "MaximumLevelOfTheMilitaryAcademyForGenerals": 0,
        "BattleWidth": 0, "UnitsAttack": 0, "UnitsDefense": 0,
        "GeneralAttack": 0, "GeneralDefense": 0, "MaxMorale": 0, "Discipline": 0,
        "Legacy": 0
    }

    def boundingRect(self): return QRectF(0,0, self.SIZE.width(), self.SIZE.height())

    def scene(self) -> TechTreeScene: return super().scene()

    def __init__(self,*,
        #/* Technology args/mods
        Name: str = "", MaintainTechnologyName: Optional[bool] = True, ImageID: int = 0,

        TreeColumn: int = 0, TreeRow: int = 0,

        RequiredTech: int = None, RequiredTech2: int = None,

        UnlocksNukes: bool = False,
        UnlocksAccessToTheSea: bool = False,

        MaximumLevelOfCapitalCity: Optional[int] = 0,
        MaximumLevelOfTheMilitaryAcademy: Optional[int] = 0,
        MaximumLevelOfTheMilitaryAcademyForGenerals: Optional[int] = 0,

        BattleWidth: Optional[int] = 0,
        UnitsAttack: Optional[int] = 0, UnitsDefense: Optional[int] = 0,
        GeneralAttack: Optional[int] = 0, GeneralDefense: Optional[int] = 0,
        MaxMorale: Optional[int] = 0, Discipline: Optional[int] = 0,

        Legacy: Optional[int] = 0,

        ResearchCost: int = 0,
        Repeatable: bool = False,
        AI: int = 5,
        **kwargs
        # Technology args/mods */
        ):
        #/* Assign technology args/mods
        self.Name, self.MaintainTechnologyName, self.ImageID = Name, MaintainTechnologyName, ImageID
        self.TreeColumn, self.TreeRow = TreeColumn, TreeRow
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

    def set_mods(self,*,
        ID: Optional[int] = None,
        Name: Optional[str] = None, MaintainTechnologyName: Optional[bool] = None, ImageID: Optional[int] = None,

        TreeColumn: Optional[int] = None, TreeRow: Optional[int] = None,

        RequiredTech: Optional[int] = None, RequiredTech2: Optional[int] = None,

        UnlocksNukes: Optional[bool] = None,
        UnlocksAccessToTheSea: Optional[bool] = None,

        MaximumLevelOfCapitalCity: Optional[int] = None,
        MaximumLevelOfTheMilitaryAcademy: Optional[int] = None,
        MaximumLevelOfTheMilitaryAcademyForGenerals: Optional[int] = None,

        BattleWidth: Optional[int] = None,
        UnitsAttack: Optional[int] = None, UnitsDefense: Optional[int] = None,
        GeneralAttack: Optional[int] = None, GeneralDefense: Optional[int] = None,
        MaxMorale: Optional[int] = None, Discipline: Optional[int] = None,

        Legacy: Optional[int] = None,

        ResearchCost: Optional[int] = None,
        Repeatable: Optional[bool] = None,
        AI: Optional[int] = None,
        **kwargs
        ):
        assign = lambda noneable, else_variant: else_variant if noneable is None else noneable

        self.scene().insert_item(assign(ID, self.ID()), self)

        self.setX(assign(TreeColumn, self.TreeColumn)); self.setY(assign(TreeRow, self.TreeRow))
        self.Name, self.MaintainTechnologyName, self.ImageID = (
            assign(Name, self.Name),
            assign(MaintainTechnologyName, self.MaintainTechnologyName),
            assign(ImageID, self.ImageID)
        )
        self.RequiredTech, self.RequiredTech2 = (
            (self.scene().tech_items[RequiredTech] if RequiredTech > -1 else None) if RequiredTech else self.RequiredTech,
            (self.scene().tech_items[RequiredTech2] if RequiredTech2 > -1 else None) if RequiredTech2 else self.RequiredTech2
        )
        self.UnlocksNukes = assign(UnlocksNukes, self.UnlocksNukes)
        self.UnlocksAccessToTheSea = assign(UnlocksAccessToTheSea, self.UnlocksAccessToTheSea)

        self.MaximumLevelOfCapitalCity = assign(MaximumLevelOfCapitalCity, self.MaximumLevelOfCapitalCity)
        self.MaximumLevelOfTheMilitaryAcademy = assign(MaximumLevelOfTheMilitaryAcademy, self.MaximumLevelOfTheMilitaryAcademy)
        self.MaximumLevelOfTheMilitaryAcademyForGenerals = assign(MaximumLevelOfTheMilitaryAcademyForGenerals, self.MaximumLevelOfTheMilitaryAcademyForGenerals)

        self.BattleWidth = assign(BattleWidth, self.BattleWidth)
        self.UnitsAttack, self.UnitsDefense = assign(UnitsAttack, self.UnitsAttack), assign(UnitsDefense, self.UnitsDefense)
        self.GeneralAttack, self.GeneralDefense = assign(GeneralAttack, self.GeneralAttack), assign(GeneralDefense, self.GeneralDefense)
        self.MaxMorale, self.Discipline = assign(MaxMorale, self.MaxMorale), assign(Discipline, self.Discipline)

        self.Legacy = assign(Legacy, self.Legacy)

        self.ResearchCost = assign(ResearchCost, self.ResearchCost)

        self.Repeatable = assign(Repeatable, self.Repeatable)
        self.AI = assign(AI,self.AI)

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

    def to_dict(self) -> dict:
        dictionary = {"ID":self.ID()}
        for mod in TechItem.MODS:
            value = getattr(self, mod)
            if mod in TechItem.MODS:
                if mod in TechItem.REQUIRED_MODS:
                    if mod in ("RequiredTech", "RequiredTech2"):
                        req_tech_id = value.ID() if value is not None else -1
                        dictionary[mod] = req_tech_id
                    elif mod != "ID":
                        dictionary[mod] = value
                elif mod in TechItem.OPTIONAL_MODS:
                    if value is not None:
                        dictionary[mod] = value
        return dictionary

    def to_compact_dict(self) -> dict:
        dictionary = {"ID":self.ID()}
        for mod in TechItem.MODS:
            value = getattr(self, mod)
            if mod in TechItem.MODS:
                if mod in TechItem.REQUIRED_MODS:
                    if mod in ("RequiredTech", "RequiredTech2"):
                        req_tech_id = value.ID() if value is not None else -1
                        dictionary[mod] = req_tech_id
                    elif mod != "ID":
                        dictionary[mod] = value
                elif mod in TechItem.OPTIONAL_MODS:
                    if value != TechItem.OPTIONAL_MODS[mod] and value is not None:
                        dictionary[mod] = value
        return dictionary