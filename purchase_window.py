import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont

import gsi_server
import purchase_log
import dota_images
import settings


class PurchaseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dota Coach — Лог покупок")
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        cfg = settings.load()
        pw = cfg["purchase_window"]
        self.setGeometry(
            pw["x"], pw["y"], pw["width"], pw["height"]
        )

        self._opacity = pw["opacity"]

        self.container = QFrame()
        self.container.setStyleSheet(
            f"background: rgba(0,0,0,{int(self._opacity * 220)}); "
            "border-radius: 8px;"
        )

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        # Заголовок
        title = QLabel("Лог покупок")
        title.setFont(QFont("Consolas", 12, QFont.Bold))
        title.setStyleSheet("color: #FFD700;")
        layout.addWidget(title)

        # ── Секция «Сейчас в инвентаре» ──
        self.inv_title = QLabel("Сейчас в инвентаре")
        self.inv_title.setStyleSheet(
            "color: #5DADE2; font-weight: bold; padding-top: 4px;"
        )
        layout.addWidget(self.inv_title)

        self.inv_scroll = QScrollArea()
        self.inv_scroll.setWidgetResizable(True)
        self.inv_scroll.setStyleSheet("background: transparent; border: none;")
        self.inv_scroll.setMaximumHeight(200)

        self.inv_content = QWidget()
        self.inv_layout = QVBoxLayout(self.inv_content)
        self.inv_layout.setAlignment(Qt.AlignTop)
        self.inv_layout.setContentsMargins(0, 0, 0, 0)
        self.inv_layout.setSpacing(2)
        self.inv_scroll.setWidget(self.inv_content)
        layout.addWidget(self.inv_scroll)

        # ── Секция «Куплено» ──
        self.log_title = QLabel("Куплено")
        self.log_title.setStyleSheet(
            "color: #27AE60; font-weight: bold; padding-top: 4px;"
        )
        layout.addWidget(self.log_title)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(2)
        self.scroll.setWidget(self.scroll_content)
        layout.addWidget(self.scroll)

        # Корневой layout
        root = QVBoxLayout()
        root.addWidget(self.container)
        self.setLayout(root)

        self.drag_pos = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)

        self._rendered_count = 0
        self._last_inv_signature = None

    # ── Перетаскивание окна ──
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        self.drag_pos = None
        # Сохранить позицию окна в config.json
        try:
            cfg = settings.load()
            cfg["purchase_window"]["x"] = self.x()
            cfg["purchase_window"]["y"] = self.y()
            settings.save(cfg)
        except Exception as e:
            print(f"[purchase_window] ошибка сохранения позиции: {e}")

    # ── Применение настроек ──
    def refresh_settings(self):
        cfg = settings.load()
        pw = cfg["purchase_window"]
        self.resize(pw["width"], pw["height"])
        self._opacity = pw["opacity"]
        self.container.setStyleSheet(
            f"background: rgba(0,0,0,{int(self._opacity * 220)}); "
            "border-radius: 8px;"
        )

    # ── Обновление ──
    def refresh(self):
        state = gsi_server.get_state()
        if not state:
            return

        purchase_log.detect_purchases(state)

        # ── Инвентарь ──
        inventory = purchase_log.get_current_inventory(state)
        inv_signature = tuple(sorted(inventory))
        if inv_signature != self._last_inv_signature:
            self._render_inventory(inventory)
            self._last_inv_signature = inv_signature

        # ── Покупки ──
        recent = purchase_log.get_recent_purchases(20)
        if len(recent) != self._rendered_count:
            self._render_purchases(recent)
            self._rendered_count = len(recent)

    # ──────────────────────────────────────────────
    #  Инвентарь
    # ──────────────────────────────────────────────
    def _clear_inventory(self):
        while self.inv_layout.count():
            item = self.inv_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def _render_inventory(self, inventory):
        self._clear_inventory()

        if not inventory:
            label = QLabel("— пусто —")
            label.setStyleSheet("color: #777; font-size: 10px;")
            self.inv_layout.addWidget(label)
            return

        # Группируем по игроку
        by_player = {}
        for player, hero, item in inventory:
            by_player.setdefault((player, hero), []).append(item)

        for (player, hero), items in by_player.items():
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(2, 2, 2, 2)
            row_layout.setSpacing(4)

            # Иконка героя
            hero_path = dota_images.hero_image_path(hero)
            if hero_path:
                h_icon = QLabel()
                pix = QPixmap(hero_path).scaled(
                    22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                h_icon.setPixmap(pix)
                h_icon.setFixedWidth(24)
                row_layout.addWidget(h_icon)

            # Имя игрока
            name_label = QLabel(player[:10])
            name_label.setStyleSheet("color: #AAA; font-size: 9px;")
            name_label.setFixedWidth(60)
            row_layout.addWidget(name_label)

            # Иконки предметов
            for item in items[:8]:
                item_path = dota_images.item_image_path(item)
                if item_path:
                    icon = QLabel()
                    pix = QPixmap(item_path).scaled(
                        22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                    icon.setPixmap(pix)
                    icon.setFixedWidth(24)
                    row_layout.addWidget(icon)

            row_layout.addStretch()
            self.inv_layout.addWidget(row)

    # ──────────────────────────────────────────────
    #  Куплено
    # ──────────────────────────────────────────────
    def _clear_layout(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _render_purchases(self, recent):
        self._clear_layout()

        if not recent:
            label = QLabel("— пока ничего не куплено —")
            label.setStyleSheet("color: #777; font-size: 10px;")
            self.scroll_layout.addWidget(label)
            return

        for entry in reversed(recent):
            self._add_entry(entry)

    def _add_entry(self, entry):
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(4, 2, 4, 2)
        row_layout.setSpacing(6)

        hero_path = dota_images.hero_image_path(entry.get("hero", ""))
        if hero_path:
            hero_icon = QLabel()
            pix = QPixmap(hero_path).scaled(
                24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            hero_icon.setPixmap(pix)
            hero_icon.setFixedWidth(26)
            row_layout.addWidget(hero_icon)

        name_label = QLabel((entry.get("player") or "?")[:10])
        name_label.setStyleSheet("color: #CCC; font-size: 10px;")
        name_label.setFixedWidth(60)
        row_layout.addWidget(name_label)

        item_path = dota_images.item_image_path(entry.get("item", ""))
        if item_path:
            item_icon = QLabel()
            pix = QPixmap(item_path).scaled(
                28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            item_icon.setPixmap(pix)
            item_icon.setFixedWidth(30)
            row_layout.addWidget(item_icon)

        item_name = (
            entry.get("item", "")
            .replace("item_", "")
            .replace("_", " ")
            .title()
        )
        item_label = QLabel(item_name)
        item_label.setStyleSheet("color: #EEE; font-size: 10px;")
        row_layout.addWidget(item_label)

        row_layout.addStretch()
        self.scroll_layout.addWidget(row)


def run_purchase_window():
    app = QApplication(sys.argv)
    window = PurchaseWindow()
    window.show()
    sys.exit(app.exec_())