from PyQt5.QtWidgets import (
    QLabel, QWidget, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap

import gsi_server
import rules
import dota_images
import settings


class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        cfg = settings.load()
        ov = cfg["overlay"]

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(ov["x"], ov["y"], ov["width"], ov["height"])

        self._opacity = ov["opacity"]
        self._font_size = ov["font_size"]

        # Колбэк для открытия меню (заполняется из main.py)
        self.open_settings_callback = None

        # Контейнер
        self.container = QFrame()
        self.container.setStyleSheet(
            f"background: rgba(0,0,0,{int(self._opacity * 210)}); "
            "border-radius: 10px;"
        )

        outer = QVBoxLayout(self.container)
        outer.setContentsMargins(10, 10, 10, 10)
        outer.setSpacing(6)

        # Заголовок
        self.header = QLabel("Ожидание Dota 2...")
        self.header.setFont(QFont("Consolas", self._font_size + 2, QFont.Bold))
        self.header.setStyleSheet("color: #FFD700;")
        self.header.setTextFormat(Qt.RichText)
        outer.addWidget(self.header)

        # Заголовок блока таймингов
        self.timings_title = QLabel("")
        self.timings_title.setStyleSheet(
            "color: #5DADE2; font-weight: bold;"
        )
        self.timings_title.setTextFormat(Qt.RichText)
        outer.addWidget(self.timings_title)

        # Контейнер строк таймингов
        self.timings_box = QVBoxLayout()
        self.timings_box.setSpacing(2)
        outer.addLayout(self.timings_box)

        # Угрозы
        self.threats_label = QLabel("")
        self.threats_label.setFont(QFont("Consolas", self._font_size))
        self.threats_label.setStyleSheet("color: #F5B7B1;")
        self.threats_label.setWordWrap(True)
        self.threats_label.setTextFormat(Qt.RichText)
        outer.addWidget(self.threats_label)

        # Общие советы
        self.general_label = QLabel("")
        self.general_label.setFont(QFont("Consolas", self._font_size))
        self.general_label.setStyleSheet("color: #D5F5E3;")
        self.general_label.setWordWrap(True)
        self.general_label.setTextFormat(Qt.RichText)
        outer.addWidget(self.general_label)

        outer.addStretch()

        # Корневой layout
        root = QVBoxLayout()
        root.addWidget(self.container)
        root.setContentsMargins(0, 0, 0, 0)
        self.setLayout(root)

        # Список виджетов-строк таймингов для очистки
        self._timing_widgets = []

        # Перетаскивание окна
        self.drag_pos = None

        # Таймер обновления
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_tips)
        self.timer.start(1000)

    # ─────────────────────────────────────────────────
    #  Перетаскивание окна
    # ─────────────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None
        # Сохранить позицию окна в config.json
        try:
            cfg = settings.load()
            cfg["overlay"]["x"] = self.x()
            cfg["overlay"]["y"] = self.y()
            settings.save(cfg)
        except Exception as e:
            print(f"[overlay] ошибка сохранения позиции: {e}")

    def mouseDoubleClickEvent(self, event):
        """Двойной клик — открыть меню."""
        if event.button() == Qt.LeftButton:
            if self.open_settings_callback:
                self.open_settings_callback()
            event.accept()

    # ─────────────────────────────────────────────────
    #  Применение настроек на лету
    # ─────────────────────────────────────────────────
    def refresh_settings(self):
        """Перечитать настройки и применить к внешнему виду."""
        cfg = settings.load()
        ov = cfg["overlay"]

        self._opacity = ov["opacity"]
        self._font_size = ov["font_size"]

        # Фон контейнера
        self.container.setStyleSheet(
            f"background: rgba(0,0,0,{int(self._opacity * 210)}); "
            "border-radius: 10px;"
        )

        # Шрифты
        self.header.setFont(
            QFont("Consolas", self._font_size + 2, QFont.Bold)
        )
        self.threats_label.setFont(QFont("Consolas", self._font_size))
        self.general_label.setFont(QFont("Consolas", self._font_size))

        # Размер окна
        self.resize(ov["width"], ov["height"])

    # ─────────────────────────────────────────────────
    #  Тайминги: строки с иконками
    # ─────────────────────────────────────────────────
    def _clear_timings(self):
        for w in self._timing_widgets:
            w.setParent(None)
            w.deleteLater()
        self._timing_widgets.clear()

    def _add_timing_row(self, tip):
        """Строка тайминга: иконка предмета + текст."""
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(2, 0, 2, 0)
        layout.setSpacing(6)

        icon_path = dota_images.item_image_path(tip.get("icon", ""))
        if icon_path:
            icon = QLabel()
            pix = QPixmap(icon_path).scaled(
                24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            icon.setPixmap(pix)
            icon.setFixedWidth(26)
            layout.addWidget(icon)

        text = QLabel()
        text.setTextFormat(Qt.RichText)
        text.setText(tip.get("html", ""))
        text.setFont(QFont("Consolas", self._font_size))
        layout.addWidget(text)
        layout.addStretch()

        self.timings_box.addWidget(row)
        self._timing_widgets.append(row)

    # ─────────────────────────────────────────────────
    #  Обновление подсказок (тик раз в секунду)
    # ─────────────────────────────────────────────────
    def update_tips(self):
        state = gsi_server.get_state()
        cfg = settings.load()
        blk = cfg["blocks"]

        # Нет данных от Dota 2
        if not state:
            self.header.setText("Ожидание Dota 2...")
            self._clear_timings()
            self.timings_title.setText("")
            self.threats_label.setText("")
            self.general_label.setText("")
            return

        clock = state.get("map", {}).get("clock_time", 0) or 0
        minutes = clock // 60
        seconds = clock % 60

        # Заголовок
        if clock < 0:
            self.header.setText("🛒 ПРЕ-ГЕЙМ")
        else:
            self.header.setText(f"COACH  {minutes:02d}:{seconds:02d}")

        # Анализ
        result = rules.analyze_grouped(state)

        # ── Тайминги ──
        self._clear_timings()
        if blk.get("timings"):
            timings = result.get("timings", [])
            if timings:
                self.timings_title.setText("⏱ Тайминги")
                for tip in timings:
                    if isinstance(tip, dict):
                        self._add_timing_row(tip)
            else:
                self.timings_title.setText("")
        else:
            self.timings_title.setText("")

        # ── Угрозы ──
        if blk.get("threats"):
            threats = result.get("threats", [])
            if threats:
                html = (
                    '<span style="color: #E74C3C; font-weight: bold;">'
                    '⚔ Угрозы врага</span><br>'
                )
                html += "<br>".join(f"  {t}" for t in threats)
                self.threats_label.setText(html)
            else:
                self.threats_label.setText("")
        else:
            self.threats_label.setText("")

        # ── Общие советы / пре-гейм ──
        if blk.get("general"):
            general = result.get("general", [])
            pre = result.get("pre_game", [])

            if pre:
                html = (
                    '<span style="color: #27AE60; font-weight: bold;">'
                    '🛒 Закуп</span><br>'
                )
                html += "<br>".join(f"  {t}" for t in pre)
                self.general_label.setText(html)
            elif general:
                html = (
                    '<span style="color: #27AE60; font-weight: bold;">'
                    '💡 Советы</span><br>'
                )
                html += "<br>".join(f"  {t}" for t in general)
                self.general_label.setText(html)
            else:
                self.general_label.setText("")
        else:
            self.general_label.setText("")


def create_overlay():
    return Overlay()