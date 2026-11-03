from PyQt6.QtWidgets import QSpinBox, QStyle, QStyleOptionSpinBox
from PyQt6.QtGui import QPainter, QPolygonF, QColor
from PyQt6.QtCore import QPointF, Qt


class ArrowSpinBox(QSpinBox):
    # a  normal  spinbox that also draws its  own  up/down triangles  on the buttons
    def paintEvent(self, event):
        super().paintEvent(event)

        opt = QStyleOptionSpinBox()
        self.initStyleOption(opt)
        style = self.style()
        up_rect  = style.subControlRect(
            QStyle.ComplexControl.CC_SpinBox, opt, QStyle.SubControl.SC_SpinBoxUp, self)
        down_rect  =   style.subControlRect(
            QStyle.ComplexControl.CC_SpinBox, opt, QStyle.SubControl.SC_SpinBoxDown, self)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#000000") if self.isEnabled() else QColor("#888888"))

        self.draw_triangle(painter,  up_rect, pointing_up=True)
        self.draw_triangle(painter, down_rect, pointing_up=False)
        painter.end()

    def draw_triangle(self, painter, rect, pointing_up):
        cx = rect.center().x() + 0.5
        cy = rect.center().y()+0.5   
        if pointing_up:
            points = [QPointF(cx - 4, cy + 2), QPointF(cx + 4, cy + 2), QPointF(cx, cy - 3)]
        else:
            points = [QPointF(cx - 4, cy - 2), QPointF(cx + 4, cy - 2), QPointF(cx, cy  +  3)]
        painter.drawPolygon(QPolygonF(points))