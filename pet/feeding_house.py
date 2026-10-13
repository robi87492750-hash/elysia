"""A small desktop house that offers virtual treats to the active pet."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QCursor, QPainter, QPixmap
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
        self._menu: QMenu | None = None
        self._screen = None
        self._art = QPixmap(str(Path(__file__).with_name("assets") / "feeding_house_garden.png"))
        self.setFixedSize(176, 176)
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setToolTip("爱莉的小院 · 点击投喂")
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

    def _feed(self, treat_id: str) -> None:
        accepted = self._on_feed(treat_id)
        self.setToolTip("投喂成功 ♡" if accepted else "先唤醒爱莉吧")
        QTimer.singleShot(2600, lambda: self.setToolTip("爱莉的小院 · 点击投喂"))

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
        if self._art.isNull():
            return
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        image = self._art.scaled(
            self.size(), Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap((self.width() - image.width()) // 2,
                           (self.height() - image.height()) // 2, image)
