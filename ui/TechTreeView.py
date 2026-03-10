import math
import weakref
from typing import Final

from PySide6.QtCore import QPoint, QPointF, Qt, QTimer, QRect, QRectF, QSizeF
from PySide6.QtGui import QPainter, QColor, Qt, QTransform, QAction, QCursor
from PySide6.QtWidgets import QGraphicsView, QLabel, QGroupBox, QGraphicsWidget, QWidget, QVBoxLayout, QMenu

ZERO_POINT: Final[QPoint] = QPoint(0,0)


def xor(*bools: bool):
    is_true = False
    for bol in bools:
        if bol:
            if is_true:
                return False
            else:
                is_true = True
    return is_true


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
        coord_type(pos.x()//TechTreeView.cell_size.x()*TechTreeView.cell_size.x()),
        coord_type(pos.y()//TechTreeView.cell_size.y()*TechTreeView.cell_size.y())
    )


def getGridPos(pos: QPoint | QPointF):
    coord_type = int if QPoint else float
    return pos.__class__(
        coord_type(pos.x()//TechTreeView.cell_size.x()),
        coord_type(pos.y()//TechTreeView.cell_size.y())
    )


def getRect(start: QPoint | QPointF, end: QPoint | QPointF):
    position = (
        start.x() if start.x() < end.x() else end.x(),
        start.y() if start.y() < end.y() else end.y())
    size = (
        abs(start.x()-end.x())+1,
        abs(start.y()-end.y())+1
    )
    return QRect(position[0], position[1], size[0], size[1])


class TechTreeView(QGraphicsView):
    from ui.TechTreeEditorWindow import TechTreeEditorWindow

    cell_size: Final[QPoint] = QPoint(200,100)

    def __init__(self, scene=None, parent:TechTreeEditorWindow=None):
        super().__init__(scene, parent)

        self.setMouseTracking(True)

        self.timer = QTimer()
        self.timer.timeout.connect(self.viewUpdate)
        self.timer.start(100)


        self.new_widget = TechTreeView.TechWidget("1")
        self.scene().addWidget(self.new_widget)
        self.new_widget.setGeometry(0,0,self.cell_size.x(),self.cell_size.y())

        self.new_widget1 = TechTreeView.TechWidget("2")
        self.scene().addWidget(self.new_widget1)
        self.new_widget1.setGeometry(self.cell_size.x(),self.cell_size.y(),self.cell_size.x(),self.cell_size.y())

        self.new_widget2 = TechTreeView.TechWidget("3")
        self.scene().addWidget(self.new_widget2)
        self.new_widget2.setGeometry(self.cell_size.x()*2,self.cell_size.y()*2,self.cell_size.x(),self.cell_size.y())


        self.center = QPoint(0,0)
        self.coordLabel = QLabel(self)

        self.scale(0.75,0.75)

        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.is_dragging = False
        self.selected: list[QGraphicsWidget] = []
        self.is_moving = False
        self.is_selecting = False
        self.start_mouse_pos = QPointF(0,0)
        self.current_mouse_pos = QPointF(0,0)

        self.setDragMode(QGraphicsView.NoDrag)

        self.centerOn(0,0)


    def viewUpdate(self):
        scene_mouse_pos = self.mapToScene(*self.current_mouse_pos.toTuple())
        self.coordLabel.setText(f"{int(scene_mouse_pos.x()/self.cell_size.x())}, {int(scene_mouse_pos.y()/self.cell_size.y())}")
        self.viewport().update()


    def getCenter(self):
        return self.mapToScene(self.viewport().rect().center())


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


        if self.is_selecting:
            painter.drawRect(getRect(self.start_mouse_pos, current_mouse_pos))

        painter.restore()


    def drawBackground(self, painter, rect):
        """Отрисовка сетки"""
        super().drawBackground(painter, rect)
        painter.save()

        painter.setPen(QColor(255, 255, 255))

        for y in range(int(self.scene().height()/self.cell_size.y())):
            painter.drawLine(
                0,
                y*self.cell_size.y(),
                math.ceil(self.scene().width()),
                y*self.cell_size.y()
            )
        painter.drawLine(0,int(self.scene().height()),int(self.scene().width()),int(self.scene().height()))

        for x in range(int(self.scene().width()/self.cell_size.x())):
            painter.drawLine(
                x*self.cell_size.x(),
                0,
                x*self.cell_size.x(),
                math.ceil(self.scene().height())
            )
        painter.drawLine(int(self.scene().width()),0,int(self.scene().width()),int(self.scene().height()))

        painter.restore()


    # При нажатии
    def mousePressEvent(self, event):
        if xor(Qt.MouseButton.LeftButton in event.buttons(), Qt.MouseButton.RightButton in event.buttons()) and not self.is_dragging:
            touchedItem = self.scene().itemAt(self.mapToScene(event.pos()), QTransform())
            if Qt.KeyboardModifier.ControlModifier not in event.modifiers() and touchedItem not in self.selected:
                for item in self.selected:
                    item.widget().setSelected(False)
                self.selected.clear()
            if touchedItem is not None:
                touchedItem.widget().setSelected(True)
                if touchedItem not in self.selected:
                    self.selected.append(touchedItem)
                if Qt.MouseButton.RightButton not in event.buttons():
                    self.is_moving = True
            else:
                self.is_selecting = True
                self.start_mouse_pos = self.mapToScene(event.pos())
                self.current_mouse_pos = event.pos()
            self.viewport().update()
        elif Qt.MouseButton.MiddleButton in event.buttons():
            self.is_dragging = True


    def select(self, start, end) -> list[QGraphicsWidget]:
        selection_rect = getRect(start,end)

        selected = []

        x = int(selection_rect.x())

        while x < int(selection_rect.x() + selection_rect.width()):
            y = int(selection_rect.y())
            while y < int(selection_rect.y() + selection_rect.height()):
                item = self.scene().itemAt(
                    QPoint(
                        int((x+0.5) * self.cell_size.x()),
                        int((y+0.5) * self.cell_size.y())
                    ),
                    QTransform()
                )
                if item is not None:
                    selected.append(item)
                y += 1
            x += 1

        return selected


    # При отпускании
    def mouseReleaseEvent(self, event):
        if xor(Qt.MouseButton.LeftButton == event.button(), Qt.MouseButton.RightButton == event.button()) and not self.is_dragging:
            if self.is_selecting:

                start_grid_pos = getGridPos(self.start_mouse_pos)
                end_grid_pos = getGridPos(self.mapToScene(event.pos()))
                selected = self.select(start_grid_pos, end_grid_pos)
                for item in selected:
                    if item not in self.selected:
                        item.widget().setSelected(True)
                        self.selected.append(item)

            self.is_selecting = False
            self.is_moving = False
            self.viewport().update()
            if Qt.MouseButton.RightButton == event.button():
                menu = QMenu()

                file_menu = menu.addMenu("Файл")
                file_menu.addAction("Новый")
                file_menu.addAction("Открыть")

                edit_menu = menu.addMenu("Правка")
                edit_menu.addAction("Копировать")
                edit_menu.addAction("Вставить")

                help_action = menu.addAction("Помощь")
                menu.exec_(QCursor.pos())
        elif Qt.MouseButton.MiddleButton == event.button():
            self.is_dragging = False


    # При движении
    def mouseMoveEvent(self, event):
        move = QPoint(
            int(self.current_mouse_pos.x()-event.x()),
            int(self.current_mouse_pos.y()-event.y())
        )
        if self.is_dragging:
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + move.x()
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + move.y()
            )
        if Qt.MouseButton.LeftButton in event.buttons() and self.is_moving:
            max_point = getQPointF(self.scene().sceneRect().size())
            scene_mouse_pos = self.mapToScene(self.current_mouse_pos)
            scene_mouse_pos = getGridedPos(
                pointClamp(scene_mouse_pos,ZERO_POINT,max_point)
            )
            next_mouse_pos = self.mapToScene(event.pos())
            next_mouse_pos = getGridedPos(
                pointClamp(next_mouse_pos,ZERO_POINT,max_point)
            )
            delta_mouse_pos = next_mouse_pos - scene_mouse_pos
            for item in self.selected:
                new_pos = item.pos()
                if (
                    0 > new_pos.x()+delta_mouse_pos.x() > self.scene().width()
                    and 0 > new_pos.x() + delta_mouse_pos.y() > self.scene().height()
                ):
                    break
            else:
                for item in self.selected:
                    item.setPos(
                        QPoint(
                            item.x()+delta_mouse_pos.x(),
                            item.y()+delta_mouse_pos.y()
                        )
                    )

        self.current_mouse_pos = event.pos()
        self.viewport().update()

    class TechWidget(QGroupBox):
        """Lazy update"""

        _instances = weakref.WeakSet()
        _dirty = False  # Флаг необходимости пересчета

        def __init__(self, name="", parent=None):
            super().__init__(name,parent)

            TechTreeView.TechWidget._instances.add(self)
            self._number = len(TechTreeView.TechWidget._instances)
            TechTreeView.TechWidget._dirty = True
            self.setStyleSheet(
                """QGroupBox {   border: 0.1em solid white; margin: 0.25em; border-radius: 20px; color: white; background-color: rgb(31,31,31);  }""")

        def __del__(self):
            TechTreeView.TechWidget._dirty = True

        def setSelected(self, is_selected: bool):
            if is_selected:
                self.setStyleSheet("""QGroupBox {   border: 0.1em solid black; margin: 0.25em; border-radius: 20px; color: black; background-color: white;  }""")
            else:
                self.setStyleSheet("""QGroupBox {   border: 0.1em solid white; margin: 0.25em; margin-top: 0.1em; border-radius: 20px; color: white; background-color: rgb(31,31,31);  }""")

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