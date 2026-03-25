import enum
import math
from functools import partial
from typing import Final

from PySide6.QtCore import QPoint, QPointF, Qt, QRect, QRectF, QSizeF, QSize
from PySide6.QtGui import QPainter, QColor, Qt, QTransform
from PySide6.QtWidgets import QGraphicsView, QLabel, QApplication, QMenu, QInputDialog

from LukaszFormatReader import format_from_lukasz, parse_dict
from ui.TechTreeScene import TechTreeScene
from ui.TechItem import TechItem


ZERO_POINT: Final[QPoint] = QPoint(0,0)


def get_q_point_f(qRectF: QRectF | QSizeF):
    return QPointF(
        qRectF.width(),
        qRectF.height()
    )


def clamp(value: int | float, minim: int | float, maxim: int | float):
    return max(min(value,maxim),minim)


def point_clamp(value: QPoint | QPointF, minim: QPoint | QPointF, maxim: QPoint | QPointF):
    coord_type = int if type(value) == QPoint else float
    return value.__class__(
        coord_type(clamp(value.x(), minim.x(), maxim.x())),
        coord_type(clamp(value.y(), minim.y(), maxim.y()))
    )


def get_grided_pos(pos: QPoint | QPointF):
    coord_type = int if type(pos) == QPoint else float
    return pos.__class__(
        coord_type(pos.x()//TechTreeScene.CELL_SIZE.width()*TechTreeScene.CELL_SIZE.width()),
        coord_type(pos.y()//TechTreeScene.CELL_SIZE.height()*TechTreeScene.CELL_SIZE.height())
    )


def get_grid_pos(pos: QPoint | QPointF):
    coord_type = int if QPoint else float
    return pos.__class__(
        coord_type(pos.x()//TechTreeScene.CELL_SIZE.width()),
        coord_type(pos.y()//TechTreeScene.CELL_SIZE.height())
    )


def get_rect(point1: QPoint | QPointF, point2: QPoint | QPointF):
    position = (
        point1.x() if point1.x() < point2.x() else point2.x(),
        point1.y() if point1.y() < point2.y() else point2.y())
    size = (
        abs(point1.x()-point2.x())+1,
        abs(point1.y()-point2.y())+1
    )
    return QRect(position[0], position[1], size[0], size[1])


class TechTreeView(QGraphicsView):

    class CursorState(enum.Enum):

        Basic = 0
        MovingScene = 1
        MovingItems = 2
        Selecting = 3

    def __init__(self, scene: TechTreeScene, parent=None):
        super().__init__(scene, parent)

        self.setMouseTracking(True)

        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setDragMode(QGraphicsView.NoDrag)

        self.coordLabel = QLabel(self)

        self.scale(0.75,0.75)

        self.cursor_state: TechTreeView.CursorState = TechTreeView.CursorState.Basic
        self.selected: list[TechItem] = []
        self.start_mouse_pos = QPoint(0,0)
        self.current_mouse_pos = QPoint(0,0)

        self.centerOn(0,0)

    def scene(self) -> TechTreeScene: return super().scene()

    def set_cursor_state(self, cursor_state: CursorState):
        self.cursor_state = cursor_state
        match cursor_state:
            case TechTreeView.CursorState.Selecting: self.setCursor(Qt.CursorShape.CrossCursor)
            case TechTreeView.CursorState.MovingScene: self.setCursor(Qt.CursorShape.OpenHandCursor)
            case TechTreeView.CursorState.MovingItems: self.setCursor(Qt.CursorShape.ClosedHandCursor)
            case TechTreeView.CursorState.Basic: self.setCursor(Qt.CursorShape.ArrowCursor)


    def resizeEvent(self, event):
        geometry = self.geometry()
        self.coordLabel.setGeometry(
            0,
            math.floor(geometry.height()-geometry.height()/20),
            math.ceil(geometry.width()),
            math.ceil(geometry.height()/20)
        )
        self.coordLabel.setStyleSheet(
        f"""
        font-size: {self.coordLabel.geometry().height()}px
        """)


    def drawForeground(self, painter, rect):
        super().drawForeground(painter, rect)

        painter.setPen(QColor(127,127,127,127))
        painter.setBrush(QColor(127,127,127,63))

        current_mouse_pos = self.mapToScene(self.current_mouse_pos.x(), self.current_mouse_pos.y())

        if self.cursor_state == TechTreeView.CursorState.Selecting:
            painter.drawRect(get_rect(self.start_mouse_pos, current_mouse_pos))

        painter.restore()


    def delete_selected(self):
        for item in self.selected:
            self.scene().removeItem(item)
            self.scene().tech_items.pop(self.scene().tech_items.index(item))
            for scn_item in self.scene().items():
                if scn_item.RequiredTech == item: scn_item.RequiredTech = None
                if scn_item.RequiredTech2 == item: scn_item.RequiredTech2 = None


    def create_new_tech(self, pos):
        tech_item = TechItem()
        self.scene().addItem(tech_item)
        tech_item.setPos(get_grid_pos(pos))


    def edit_tech(self, tech: TechItem):
        dictionary = tech.to_dict()
        text = "{\n"
        for key in dictionary.keys():
            value = None
            predict = dictionary[key]
            if isinstance(predict, str): value = f'"{dictionary[key]}"'
            elif isinstance(predict, bool): value = "true" if dictionary[key] else "false"
            else: value = dictionary[key]

            text += f"    {key}: {value},\n"
        text += "}"
        text, ok = QInputDialog.getMultiLineText(self, 'Edit technology', 'Technology', text)
        if ok:
            dictionary = {}
            content = parse_dict(format_from_lukasz(text))
            if isinstance(content, dict):
                for key in content.keys():
                    value = content[key]
                    if key in TechItem.MODS:
                        # print(key, value)
                        if key in TechItem.REQUIRED_MODS:
                            if isinstance(value, TechItem.REQUIRED_MODS[key]):
                                dictionary[key] = value
                        elif key in TechItem.OPTIONAL_MODS:
                            if value is not None:
                                if isinstance(value, type(TechItem.OPTIONAL_MODS[key])):
                                    dictionary[key] = value
                tech.set_mods(**dictionary)
            else:
                raise TypeError(f"Content is {type(content)}")



    def open_context_menu(self, pos, global_pos):
        touched_item = self.scene().itemAt(self.mapToScene(pos),QTransform())
        menu = QMenu("Menu",self)
        menu.setStyleSheet("border-radius: 0.25em; background-color: black")
        if touched_item:
            menu.addAction("Edit", partial(lambda: [self.edit_tech(tech) for tech in self.selected]))
            menu.addAction("Delete", partial(self.delete_selected))
            last_id = len(self.scene().tech_items)-1
            if len(self.selected) < 2:
                menu.addAction(f"Set ID = {last_id}", partial(self.scene().insert_item, last_id, touched_item))
                menu.addAction(f"Set ID = 0", partial(self.scene().insert_item, 0, touched_item))
        else:
            menu.addAction("Create new", partial(self.create_new_tech,self.mapToScene(pos)))
        geo = menu.geometry()
        size = QSize(
            geo.width(),
            geo.height()*len(menu.actions())
        )
        menu.setGeometry(QRect(global_pos,size))
        menu.show()


    def scroll_bars(self, delta_pos: QPoint | QPointF):
        self.horizontalScrollBar().setValue(
            int(self.horizontalScrollBar().value() + delta_pos.x()))
        self.verticalScrollBar().setValue(
            int(self.verticalScrollBar().value() + delta_pos.y()))


    def clear_selected(self):
        if len(self.selected) > 0:
            for item in self.selected:
                item.set_selected(False)
            self.selected.clear()


    def deselect(self, item):
        if item in self.selected:
            item.set_selected(False)
            self.selected.pop(self.selected.index(item))


    def select(self, item, ctrl_mod=False):
        if not ctrl_mod:
            self.clear_selected()
        if item not in self.selected:
            if item:
                item.set_selected(True)
                self.selected.append(item)


    def start_selecting(self, start_pos: QPoint, mod: bool=False):
        if not mod:
            self.clear_selected()
        self.set_cursor_state(TechTreeView.CursorState.Selecting)
        self.start_mouse_pos = start_pos


    def end_selecting(self, last_pos: QPoint, alt_mod=False):
        self.set_cursor_state(TechTreeView.CursorState.Basic)
        point1 = get_grid_pos(self.start_mouse_pos)
        point2 = get_grid_pos(last_pos)
        self.start_mouse_pos = last_pos

        selection_rect = get_rect(point1, point2)

        x = int(selection_rect.x())
        while x < int(selection_rect.x() + selection_rect.width()):
            y = int(selection_rect.y())
            while y < int(selection_rect.y() + selection_rect.height()):
                item = self.scene().itemAt(
                    QPoint(
                        int((x + 0.5) * TechTreeScene.CELL_SIZE.width()),
                        int((y + 0.5) * TechTreeScene.CELL_SIZE.height())
                    ), QTransform()
                )
                if item is not None:
                    if alt_mod:
                        self.deselect(item)
                    else:
                        self.select(item, True)
                y += 1
            x += 1
        self.viewport().update()


    # Mouse button down
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        buttons = event.buttons()
        scene_mouse_pos = self.mapToScene(event.pos())
        touchedItem = self.scene().itemAt(scene_mouse_pos, QTransform())
        ctrl_mod = Qt.KeyboardModifier.ControlModifier in event.modifiers()
        alt_mod = Qt.KeyboardModifier.AltModifier in event.modifiers()
        # Middle button
        if Qt.MouseButton.MiddleButton in buttons:
            if self.cursor_state == TechTreeView.CursorState.Selecting:
                self.end_selecting(scene_mouse_pos)
            self.set_cursor_state(TechTreeView.CursorState.MovingScene)
        # Right button
        elif Qt.MouseButton.RightButton in buttons:
            if self.cursor_state == TechTreeView.CursorState.Selecting:
                self.end_selecting(scene_mouse_pos)
            if touchedItem in self.selected:
                pass
            else:
                self.select(touchedItem, False)
        # Left button
        elif Qt.MouseButton.LeftButton in buttons:
            # Click on item
            if touchedItem:
                if touchedItem in self.selected:
                    if alt_mod:
                        self.deselect(touchedItem)
                else:
                    if not alt_mod:
                        self.select(touchedItem, ctrl_mod)
                self.set_cursor_state(TechTreeView.CursorState.MovingItems)
            # Click on scene
            else:
                if self.cursor_state not in (TechTreeView.CursorState.MovingScene, TechTreeView.CursorState.MovingItems):
                    self.start_selecting(self.mapToScene(event.pos()), ctrl_mod or alt_mod)
        self.current_mouse_pos = event.pos()
        event.accept()
        self.viewport().update()


    # Mouse button up
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        mouse_pos = event.pos()
        scene_mouse_pos = self.mapToScene(mouse_pos)
        touchedItem = self.scene().itemAt(event.pos(), QTransform())
        match event.button():
            case Qt.MouseButton.MiddleButton:
                if self.cursor_state == TechTreeView.CursorState.MovingScene:
                    self.set_cursor_state(TechTreeView.CursorState.Basic)
            case Qt.MouseButton.LeftButton:
                match self.cursor_state:
                    case TechTreeView.CursorState.Selecting:
                        self.end_selecting(scene_mouse_pos, Qt.KeyboardModifier.AltModifier in event.modifiers())
                    case TechTreeView.CursorState.MovingItems:
                        self.set_cursor_state(TechTreeView.CursorState.Basic)
            case Qt.MouseButton.RightButton:
                self.open_context_menu(event.pos(), event.globalPos())
        event.accept()
        self.viewport().update()


    # Mouse move
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        mouse_pos = event.pos()
        buttons = event.buttons()
        scene_event_pos = self.mapToScene(event.pos())
        self.coordLabel.setText(f"{int(scene_event_pos.x()/TechTreeScene.CELL_SIZE.width())}, {int(scene_event_pos.y()/TechTreeScene.CELL_SIZE.height())}")
        delta_mouse_pos = QPoint(
            math.ceil(self.current_mouse_pos.x()-event.x()),
            math.ceil(self.current_mouse_pos.y()-event.y())
        )
        if Qt.MouseButton.MiddleButton in buttons and self.cursor_state == TechTreeView.CursorState.MovingScene:
            self.scroll_bars(delta_mouse_pos)
        if Qt.MouseButton.LeftButton in buttons:
            if self.cursor_state == TechTreeView.CursorState.MovingItems:
                max_point = get_q_point_f(self.scene().sceneRect().size())
                scene_mouse_pos = self.mapToScene(self.current_mouse_pos)
                scene_mouse_pos = get_grided_pos(
                    point_clamp(scene_mouse_pos, ZERO_POINT, max_point)
                )
                next_mouse_pos = get_grided_pos(
                    point_clamp(scene_event_pos, ZERO_POINT, max_point)
                )
                delta_mouse_pos = next_mouse_pos - scene_mouse_pos

                for item in self.selected:
                    new_pos = item.pos()
                    if 0 > new_pos.x()+delta_mouse_pos.x() or new_pos.x() + delta_mouse_pos.x() > self.scene().width():
                        delta_mouse_pos.setX(0)
                    if 0 > new_pos.y() + delta_mouse_pos.y() or new_pos.y() + delta_mouse_pos.y() > self.scene().height():
                        delta_mouse_pos.setY(0)

                for item in self.selected:
                    item.setPos(
                        get_grid_pos(
                            QPoint(
                                (item.x() + delta_mouse_pos.x()),
                                (item.y() + delta_mouse_pos.y())
                            )
                        )
                    )
        self.current_mouse_pos = mouse_pos
        event.accept()
        self.viewport().update()


    def wheelEvent(self, event):
        delta = (event.angleDelta().x() + event.angleDelta().y())/1000
        x, y = self.transform().m11(), self.transform().m22()
        value = clamp((x+y)/2.0+delta,0.2,1.0)
        self.scale(1/x,1/y)
        self.scale(value,value)

    def export(self) -> str:
        scene = self.scene()
        content = ''
        for tech in scene.tech_items:
            dictionary = tech.to_compact_dict()
            content += "        {\n"
            for key in dictionary.keys():
                value = None
                predict = dictionary[key]
                if isinstance(predict, str):
                    value = f'"{dictionary[key]}"'
                elif isinstance(predict, bool):
                    value = "true" if dictionary[key] else "false"
                else:
                    value = dictionary[key]
                content += f"           {key}: {value},\n"
            content += "        },\n"
        return content