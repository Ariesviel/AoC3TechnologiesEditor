import enum
import math
import weakref
from typing import Final

from PySide6.QtCore import QPoint, QPointF, Qt, QRect, QRectF, QSizeF, QSize
from PySide6.QtGui import QPainter, QColor, Qt, QTransform
from PySide6.QtWidgets import QGraphicsView, QLabel, QWidget, QGraphicsItem, QApplication

ZERO_POINT: Final[QPoint] = QPoint(0,0)


def getQPointF(qRectF: QRectF | QSizeF):
    return QPointF(
        qRectF.width(),
        qRectF.height()
    )


def clamp(value: int | float, minim: int | float, maxim: int | float):
    return max(min(value,maxim),minim)


def pointClamp(value: QPoint | QPointF, minim: QPoint | QPointF, maxim: QPoint | QPointF):
    coord_type = int if type(value) == QPoint else float
    return value.__class__(
        coord_type(max(min(value.x(), maxim.x()), minim.x())),
        coord_type(max(min(value.y(), maxim.y()), minim.y()))
    )


def getGridedPos(pos: QPoint | QPointF):
    coord_type = int if type(pos) == QPoint else float
    return pos.__class__(
        coord_type(pos.x()//TechTreeView.cell_size.width()*TechTreeView.cell_size.width()),
        coord_type(pos.y()//TechTreeView.cell_size.height()*TechTreeView.cell_size.height())
    )


def getGridPos(pos: QPoint | QPointF):
    coord_type = int if QPoint else float
    return pos.__class__(
        coord_type(pos.x()//TechTreeView.cell_size.width()),
        coord_type(pos.y()//TechTreeView.cell_size.height())
    )


def getRect(point1: QPoint | QPointF, point2: QPoint | QPointF):
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

    from ui.TechTreeEditorWindow import TechTreeEditorWindow

    cell_size: Final[QSize] = QSize(300,100)

    def __init__(self, scene=None, parent:TechTreeEditorWindow=None):
        super().__init__(scene, parent)

        self.setMouseTracking(True)

        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setDragMode(QGraphicsView.NoDrag)

        self.new_widget = TechTreeView.TechWidget("1")
        self.scene().addWidget(self.new_widget)

        self.new_widget1 = TechTreeView.TechWidget("2")
        self.scene().addWidget(self.new_widget1)
        geo = self.new_widget1.geometry()
        self.new_widget1.setGeometry(self.cell_size.width(),self.cell_size.height(),geo.width(),geo.height())

        self.coordLabel = QLabel(self)

        self.scale(0.75,0.75)

        self.cursor_state: TechTreeView.CursorState = TechTreeView.CursorState.Basic
        self.selected: list[QGraphicsItem] = []
        self.start_mouse_pos = QPoint(0,0)
        self.current_mouse_pos = QPoint(0,0)

        self.centerOn(0,0)


    def setCursorState(self, state: CursorState):
        self.cursor_state = state
        match state:
            case TechTreeView.CursorState.Selecting:
                QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
            case TechTreeView.CursorState.MovingScene:
                QApplication.setOverrideCursor(Qt.CursorShape.OpenHandCursor)
            case TechTreeView.CursorState.MovingItems:
                QApplication.setOverrideCursor(Qt.CursorShape.ClosedHandCursor)
            case TechTreeView.CursorState.Basic:
                QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)


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
        """Отрисовка области выделения"""
        super().drawForeground(painter, rect)
        painter.save()

        painter.setPen(QColor(127,127,127,127))
        painter.setBrush(QColor(127,127,127,63))

        current_mouse_pos = self.mapToScene(self.current_mouse_pos.x(), self.current_mouse_pos.y())

        if self.cursor_state == TechTreeView.CursorState.Selecting:
            painter.drawRect(getRect(self.start_mouse_pos, current_mouse_pos))

        painter.restore()


    def drawBackground(self, painter, rect):
        """Отрисовка сетки"""
        super().drawBackground(painter, rect)
        painter.save()

        painter.setPen(QColor(255, 255, 255))

        for y in range(int(self.scene().height()/self.cell_size.height())):
            painter.drawLine(
                0,
                y*self.cell_size.height(),
                math.ceil(self.scene().width()),
                y*self.cell_size.height()
            )
        painter.drawLine(0,int(self.scene().height()),int(self.scene().width()),int(self.scene().height()))

        for x in range(int(self.scene().width()/self.cell_size.width())):
            painter.drawLine(
                x*self.cell_size.width(),
                0,
                x*self.cell_size.width(),
                math.ceil(self.scene().height())
            )
        painter.drawLine(int(self.scene().width()),0,int(self.scene().width()),int(self.scene().height()))

        painter.restore()


    def scrollBars(self, dpos: QPoint | QPointF):
        self.horizontalScrollBar().setValue(
            int(self.horizontalScrollBar().value() + dpos.x())
        )
        self.verticalScrollBar().setValue(
            int(self.verticalScrollBar().value() + dpos.y())
        )


    def startSelecting(self, start_pos: QPoint, ctrl_mod: bool=False):
        if not ctrl_mod:
            self.selected.clear()
        self.setCursorState(TechTreeView.CursorState.Selecting)
        self.start_mouse_pos = start_pos


    def endSelect(self, last_pos: QPoint):
        self.setCursorState(TechTreeView.CursorState.Basic)
        point1 = getGridPos(self.start_mouse_pos)
        point2 = getGridPos(last_pos)

        selection_rect = getRect(point1, point2)

        x = int(selection_rect.x())
        while x < int(selection_rect.x() + selection_rect.width()):
            y = int(selection_rect.y())
            while y < int(selection_rect.y() + selection_rect.height()):
                item = self.scene().itemAt(
                    QPoint(
                        int((x + 0.5) * self.cell_size.width()),
                        int((y + 0.5) * self.cell_size.height())
                    ),
                    QTransform()
                )
                if item is not None:
                    if item not in self.selected:
                        self.selected.append(item)
                y += 1
            x += 1
        self.viewport().update()


    # При нажатии
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        buttons = event.buttons()
        scene_mouse_pos = self.mapToScene(event.pos())
        touchedItem = self.scene().itemAt(scene_mouse_pos, QTransform())
        ctrl_mod = Qt.KeyboardModifier.ControlModifier in event.modifiers()
        if Qt.MouseButton.MiddleButton in buttons:
            if self.cursor_state == TechTreeView.CursorState.Selecting:
                self.endSelect(scene_mouse_pos)
            self.setCursorState(TechTreeView.CursorState.MovingScene)
        elif Qt.MouseButton.RightButton in buttons:
            if self.cursor_state == TechTreeView.CursorState.Selecting:
                self.endSelect(scene_mouse_pos)
        elif Qt.MouseButton.LeftButton in buttons:
            if touchedItem:
                if touchedItem not in self.selected:
                    if not ctrl_mod:
                        self.selected.clear()
                    self.selected.append(touchedItem)
                self.setCursorState(TechTreeView.CursorState.MovingItems)
            else:
                if self.cursor_state not in (TechTreeView.CursorState.MovingScene, TechTreeView.CursorState.MovingItems):
                    self.startSelecting(self.mapToScene(event.pos()), ctrl_mod)


    def wheelEvent(self, event):
        delta = (event.angleDelta().x() + event.angleDelta().y())/1000
        x, y = self.transform().m11(), self.transform().m22()
        value = clamp((x+y)/2.0+delta,0.25,1.0)
        self.scale(1/x,1/y)
        self.scale(value,value)
        print(value)


    # При отпускании
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        mouse_pos = event.pos()
        scene_mouse_pos = self.mapToScene(mouse_pos)
        touchedItem = self.scene().itemAt(event.pos(), QTransform())
        match event.button():
            case Qt.MouseButton.MiddleButton:
                if self.cursor_state == TechTreeView.CursorState.MovingScene:
                    self.setCursorState(TechTreeView.CursorState.Basic)
            case Qt.MouseButton.LeftButton:
                match self.cursor_state:
                    case TechTreeView.CursorState.Selecting:
                        self.endSelect(scene_mouse_pos)
                    case TechTreeView.CursorState.MovingItems:
                        self.setCursorState(TechTreeView.CursorState.Basic)


    # При движении
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        mouse_pos = event.pos()
        buttons = event.buttons()
        scene_event_pos = self.mapToScene(event.pos())
        self.coordLabel.setText(f"{int(scene_event_pos.x()/self.cell_size.width())}, {int(scene_event_pos.y()/self.cell_size.height())}")
        delta_mouse_pos = QPoint(
            math.ceil(self.current_mouse_pos.x()-event.x()),
            math.ceil(self.current_mouse_pos.y()-event.y())
        )
        if Qt.MouseButton.MiddleButton in buttons and self.cursor_state == TechTreeView.CursorState.MovingScene:
            self.scrollBars(delta_mouse_pos)
        if Qt.MouseButton.LeftButton in buttons:
            if self.cursor_state == TechTreeView.CursorState.MovingItems:
                max_point = getQPointF(self.scene().sceneRect().size())
                scene_mouse_pos = self.mapToScene(self.current_mouse_pos)
                scene_mouse_pos = getGridedPos(
                    pointClamp(scene_mouse_pos,ZERO_POINT,max_point)
                )
                next_mouse_pos = getGridedPos(
                    pointClamp(scene_event_pos,ZERO_POINT,max_point)
                )
                delta_mouse_pos = next_mouse_pos - scene_mouse_pos
                for item in self.selected:
                    new_pos = item.pos()
                    if 0 > new_pos.x()+delta_mouse_pos.x() or new_pos.x()+delta_mouse_pos.x() > self.scene().width():
                        delta_mouse_pos.setX(0)
                    if 0 > new_pos.y() + delta_mouse_pos.y() or new_pos.y() + delta_mouse_pos.y() > self.scene().height():
                        delta_mouse_pos.setY(0)
                else:
                    for item in self.selected:
                        item.setPos(
                            QPoint(
                                item.x()+delta_mouse_pos.x(),
                                item.y()+delta_mouse_pos.y()
                            )
                        )

        self.current_mouse_pos = mouse_pos
        self.viewport().update()


    class TechWidget(QWidget):
        """Lazy update. Большую часть сгенила ИИшка"""

        _instances = weakref.WeakSet()
        _dirty = False  # Флаг необходимости пересчета

        def __init__(self, name="", /, pos=QPoint(0,0), parent=None):
            super().__init__(parent)
            w, h = TechTreeView.cell_size.width(), TechTreeView.cell_size.height()
            self.setGeometry(pos.x(),pos.y(),w,h)

            self.label = QLabel(self)
            self.label.setText(name)
            self.label.setGeometry(0,0,self.width(),math.floor(self.height()/3))
            self.label.setStyleSheet(f"""font-size: {math.floor(self.height()/4)}px; background-color: rgba(127,127,127,63) """)

            TechTreeView.TechWidget._instances.add(self)
            self._number = len(TechTreeView.TechWidget._instances)
            TechTreeView.TechWidget._dirty = True
            self.setStyleSheet(
                """QWidget {   color: white; background-color: rgb(31,31,31);  }""")

        def __del__(self):
            TechTreeView.TechWidget._dirty = True

        def setSelected(self, is_selected: bool):
            if is_selected:
                self.setStyleSheet("""QWidget {   color: black; background-color: white;  }""")
            else:
                self.setStyleSheet("""QWidget {   color: white; background-color: rgb(31,31,31);  }""")

        @property
        def number(self):
            """Ленивое обновление номера при запросе"""
            if TechTreeView.TechWidget._dirty:
                self.__class__._recalculate_numbers()
            return self._number

        @classmethod
        def _recalculate_numbers(cls):
            """Пересчитывает номера только при необходимости"""
            if not cls._dirty:
                return

            instances = list(cls._instances)
            for i, instance in enumerate(instances, 1):
                instance._number = i

            cls._dirty = False

        @classmethod
        def get_all_sorted(cls):
            """Получить все с гарантией актуальности номеров"""
            cls._recalculate_numbers()
            instances = list(cls._instances)
            instances.sort(key=lambda x: x._number)
            return instances