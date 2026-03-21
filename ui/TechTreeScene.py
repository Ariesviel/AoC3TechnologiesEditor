import math
from typing import Final

from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QGraphicsScene

from LukaszFormatReader import format_type


class TechTreeScene(QGraphicsScene):

    CELL_SIZE: Final[QSize] = QSize(450, 150)

    def __init__(self, file_path=None):
        super().__init__(0,0,self.CELL_SIZE.width()*200,self.CELL_SIZE.height()*100)
        #/* Technologies extraction
        from ui.TechItem import TechItem
        self.tech_items: list[TechItem] = []
        if file_path:
            content = format_type("Technology", file_path)
            for technology in content["Technology"]:
                self.addItem(TechItem(**technology))
        for techItem in self.tech_items:
            techItem.RequiredTech = self.tech_items[techItem.RequiredTech] if techItem.RequiredTech > -1 else None
            techItem.RequiredTech2 = self.tech_items[techItem.RequiredTech2] if techItem.RequiredTech2 > -1 else None
        # Technologies extraction */


    def addItem(self, item, /):
        super().addItem(item)
        self.tech_items.append(item)


    def draw_grid(self, painter: QPainter):
        w, h = self.CELL_SIZE.width(), self.CELL_SIZE.height()

        painter.setPen(QColor(35, 35, 35))
        painter.setBrush(QColor(35, 35, 35))

        painter.drawRect(self.sceneRect())

        painter.setPen(QColor(191, 191, 191))
        painter.setBrush(QColor(191, 191, 191))

        #/* Horizontal lines
        for y in range(math.ceil(self.height()/h)):
            painter.drawLine(
                0,
                y*h,
                math.ceil(self.width()),
                y*h
            )
        painter.drawLine(0,int(self.height()),int(self.width()),int(self.height()))
        # Horizontal lines */

        #/* Vertical lines
        for x in range(math.ceil(self.width()/w)):
            painter.drawLine(
                x*w,
                0,
                x*w,
                math.ceil(self.height())
            )
        painter.drawLine(int(self.width()),0,int(self.width()),int(self.height()))
        # Vertical lines */


    @staticmethod
    def draw_tech_line(painter: QPainter, start: QPoint, end: QPoint, w: float, color: QColor):
        painter.setPen(color)
        painter.setBrush(color)
        point1 = QPoint(
            int(end.x()-w*0.125),
            start.y()
        )
        painter.drawLine(start,point1)
        point2 = QPoint(
            int(end.x()-w*0.025),
            end.y()
        )
        painter.drawLine(point1,point2)
        painter.drawLine(point2,end)


    def draw_tech_lines(self, painter: QPainter):
        for techItem in self.tech_items:
            #/* Line for RequiredTech
            tech1 = techItem.RequiredTech
            if tech1:
                end1 = QPoint(
                    techItem.x()+tech1.OFFSET,
                    techItem.y()+techItem.SIZE.height()/4+tech1.OFFSET
                )
                start1 = QPoint(
                    tech1.x()+tech1.SIZE.width()+tech1.OFFSET,
                    tech1.y()+tech1.SIZE.height()/4+tech1.OFFSET
                )
                self.draw_tech_line(painter, start1, end1, tech1.SIZE.width(), QColor(0, 255, 255))
            # Line for RequiredTech */

            #/* Line for RequiredTech2
            tech2 = techItem.RequiredTech2
            if tech2:
                end2 = QPoint(
                    techItem.x()+tech2.OFFSET,
                    techItem.y()+3*techItem.SIZE.height()/4+tech2.OFFSET
                )
                start2 = QPoint(
                    tech2.x()+tech2.SIZE.width()+tech2.OFFSET,
                    tech2.y()+3*tech2.SIZE.height()/4+tech2.OFFSET
                )
                self.draw_tech_line(painter, start2, end2, tech2.SIZE.width(), QColor(0, 255, 0))
            # Line for RequiredTech2 */


    def drawBackground(self, painter, rect, /):
        super().drawBackground(painter, rect)

        #/* Background
        painter.setPen(QColor(35, 35, 35))
        painter.setBrush(QColor(35, 35, 35))
        painter.drawRect(0,0,self.width(),self.height())
        # Background */

        self.draw_grid(painter)
        self.draw_tech_lines(painter)

        painter.restore()