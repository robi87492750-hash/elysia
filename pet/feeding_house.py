"""A small desktop house that offers virtual treats to the active pet."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QPoint, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QCursor, QFont, QLinearGradient, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QApplication, QMenu, QWidget


TREATS = (
    ("strawberry", "🍓 草莓", "草莓好甜呀，谢谢舰长♪"),
    ("cake", "🍰 小蛋糕", "啊呜～蛋糕是给我的吗？好开心♪"),
    ("milk", "🥛 热牛奶", "暖暖的牛奶，陪我再待一会儿吧♪"),
)


class FeedingHouse(QWidget):
    """An always visible, screen-corner entrance to the feeding menu."""

    def __init__(self, app: QApplication, on_feed: Callable[[str], bool]) -> None:
        super().__init__(None)
        self._app = app
        self._on_feed = on_feed
        self._caption = "爱莉的小屋"
        self._menu: QMenu | None = None
        self._screen = None
        self.setFixedSize(112, 116)
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setToolTip("爱莉的小屋 · 点击投喂")
        self._caption_timer = QTimer(self)
        self._caption_timer.setSingleShot(True)
        self._caption_timer.timeout.connect(self._reset_caption)
        self._attach_screen(app.primaryScreen())
        app.primaryScreenChanged.connect(self._attach_screen)

    def _attach_screen(self, screen) -> None:
        if self._screen is not None:
            try:
                self._screen.availableGeometryChanged.disconnect(self._place)
            except (RuntimeError, TypeError):
                pass
        self._screen = screen
        if screen is not None:
            screen.availableGeometryChanged.connect(self._place)
        self._place()

    def _place(self, *_args) -> None:
        screen = self._screen or self._app.primaryScreen()
        if screen is None:
            return
        area = screen.availableGeometry()
        self.move(area.right() - self.width() - 13,
                  area.bottom() - self.height() - 12)

    def _reset_caption(self) -> None:
        self._caption = "爱莉的小屋"
        self.update()

    def _feed(self, treat_id: str) -> None:
        accepted = self._on_feed(treat_id)
        self._caption = "投喂成功 ♡" if accepted else "先唤醒爱莉吧"
        self.update()
        self._caption_timer.start(2600)

    def _open_menu(self) -> None:
        if self._menu is not None:
            self._menu.close()
            self._menu.deleteLater()
        menu = QMenu(self)
        menu.setTitle("给爱莉投喂")
        menu.setStyleSheet(
            "QMenu { background: #fff7fb; color: #6f3856; border: 1px solid #e9a8c8; "
            "border-radius: 12px; padding: 7px; font-size: 13px; }"
            "QMenu::item { padding: 7px 20px 7px 12px; border-radius: 7px; }"
            "QMenu::item:selected { background: #f7d8e9; }"
        )
        for treat_id, label, _bubble in TREATS:
            menu.addAction(label, lambda _checked=False, name=treat_id: self._feed(name))
        self._menu = menu
        menu.popup(self.mapToGlobal(QPoint(0, -menu.sizeHint().height() - 5)))

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() in (Qt.MouseButton.LeftButton, Qt.MouseButton.RightButton):
            self._open_menu()
            event.accept()
            return
        super().mousePressEvent(event)

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        shadow = QColor(96, 49, 76, 38)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(shadow)
        painter.drawEllipse(QRectF(15, 103, 87, 9))

        roof = QPainterPath()
        roof.moveTo(13, 54)
        roof.quadTo(54, 9, 58, 15)
        roof.quadTo(65, 9, 103, 54)
        roof.quadTo(108, 63, 98, 64)
        roof.lineTo(18, 64)
        roof.quadTo(8, 63, 13, 54)
        gradient = QLinearGradient(14, 20, 100, 65)
        gradient.setColorAt(0, QColor("#f9bfd9"))
        gradient.setColorAt(1, QColor("#d66eaa"))
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor("#af4c82"), 2))
        painter.drawPath(roof)

        painter.setBrush(QColor("#fff3e9"))
        painter.setPen(QPen(QColor("#d99bb9"), 2))
        painter.drawRoundedRect(QRectF(23, 57, 69, 43), 8, 8)
        painter.setBrush(QColor("#bd6a94"))
        painter.drawRoundedRect(QRectF(48, 70, 20, 30), 9, 9)
        painter.setBrush(QColor("#fff9ef"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(61, 84, 3, 3))

        heart = QPainterPath()
        heart.moveTo(57, 48)
        heart.cubicTo(44, 38, 45, 55, 57, 59)
        heart.cubicTo(69, 55, 70, 38, 57, 48)
        painter.setBrush(QColor("#fff9fd"))
        painter.drawPath(heart)

        painter.setPen(QColor("#754565"))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QRectF(1, 0, 110, 22), Qt.AlignmentFlag.AlignCenter, self._caption)
