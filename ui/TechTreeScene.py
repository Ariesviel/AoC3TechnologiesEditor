import math
from typing import Final

from PySide6.QtCore import QSize, QPoint, QRect
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsScene

from LukaszFormatReader import format_type


class TechTreeScene(QGraphicsScene):

    CELL_SIZE: Final[QSize] = QSize(600, 200)
    
    def __init__(self, file=None):
        super().__init__(QRect(QPoint(0,0), self.CELL_SIZE*100))
        if file is not None:
            content = format_type("Technology", file)
            technologies = content['Technology']
            for technology in technologies:
                self.dict_to_tech_stats(technology)


    def dict_to_tech_stats(self, dictionary: dict):
        from ui.TechWidget import TechWidget
        from ui.TechStats import TechStats
        widget = TechWidget(TechStats(**dictionary), QPoint(dictionary["TreeColumn"], dictionary["TreeRow"]))
        self.addWidget(widget)


    def drawBackground(self, painter, rect):
        """Отрисовка сетки"""
        super().drawBackground(painter, rect)
        painter.save()

        painter.setPen(QColor(255, 255, 255))
        painter.setBrush(QColor(255, 255, 255))

        w, h = self.CELL_SIZE.width(), self.CELL_SIZE.height()

        for y in range(math.ceil(self.height()/self.CELL_SIZE.height())):
            painter.drawLine(
                0,
                y*self.CELL_SIZE.height(),
                math.ceil(self.width()),
                y*self.CELL_SIZE.height()
            )
        painter.drawLine(0,int(self.height()),int(self.width()),int(self.height()))

        for x in range(math.ceil(self.width()/self.CELL_SIZE.width())):
            painter.drawLine(
                x*self.CELL_SIZE.width(),
                0,
                x*self.CELL_SIZE.width(),
                math.ceil(self.height())
            )
        painter.drawLine(int(self.width()),0,int(self.width()),int(self.height()))

        techs = {}

        for widget in self.items():
            techs[widget.widget().tech_stats.ID] = widget

        for widget in self.items():
            tech = widget.widget().tech_stats.RequiredTech
            tech2 = widget.widget().tech_stats.RequiredTech2
            wid = widget.widget()
            end = QPoint(
                widget.x(),
                int(widget.y()+wid.height()/4)
            )
            end2 = QPoint(
                widget.x(),
                int(widget.y()+3*wid.height()/4)
            )
            if tech > -1:
                painter.setBrush(QColor(0,255,255))
                painter.setPen(QColor(0,255,255))
                tech_proxy = techs[tech]
                tech_wid = tech_proxy.widget()
                start = QPoint(
                    tech_proxy.x()+tech_wid.width(),
                    int(tech_proxy.y()+tech_wid.height()/4)
                )
                point1 = QPoint(
                    int(start.x()+w*0.05),
                    start.y()
                )
                point2 = QPoint(
                    int(point1.x()+w*0.1),
                    end.y()
                )
                painter.drawLine(start, point1)
                painter.drawLine(point1, point2)
                painter.drawLine(point2, end)
            if tech2 > -1:
                painter.setBrush(QColor(0,255,0))
                painter.setPen(QColor(0,255,0))
                tech_proxy = techs[tech2]
                tech_wid = tech_proxy.widget()
                start = QPoint(
                    tech_proxy.x()+tech_wid.width(),
                    int(tech_proxy.y()+tech_wid.height()/4)
                )
                point1 = QPoint(
                    int(start.x()+w*0.05),
                    start.y()
                )
                point2 = QPoint(
                    int(point1.x()+w*0.1),
                    end2.y()
                )
                painter.drawLine(start, point1)
                painter.drawLine(point1, point2)
                painter.drawLine(point2, end2)

        painter.restore()


    from ui.TechWidget import TechWidget
    def addWidget(self, widget: TechWidget, /, wFlags=...):
        if wFlags is ...:
            super().addWidget(widget)
        else:
            super().addWidget(widget, wFlags=wFlags)