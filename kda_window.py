from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont

import gsi_server
import kda_tracker
import dota_images
import settings


TREND_UP = "#2ECC71"
TREND_DOWN = "#E74C3C"
TREND_FLAT = "#888888"

RANK_COLORS = ["#FFD700", "#C0C0C0", "#CD7F32", "#AAAAAA"]


class KDAWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dota Coach — KDA")
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        cfg = settings.load()
        kw = cfg["kda_window"]
        self.setGeometry(
            kw["x"], kw["y"], kw["width"], kw["height"]
        )

        self._opacity = kw["opacity"]

        self.container = QFrame()
        self.container.setStyleSheet(
            f"background: rgba(0,0,0,{int(self._opacity * 220)}); "
            "border-radius: 8px;"
        )

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(4)

        title = QLabel("KDA — таблица ценности")
        title.setFont(QFont("Consolas", 12, QFont.Bold))
        title.setStyleSheet("color: #FFD700; padding-bottom: 4px;")
        layout.addWidget(title)

        self.rows_layout = QVBoxLayout()
        self.rows_layout.setSpacing(2)
        self.rows_layout.setAlignment(Qt.AlignTop)
        layout.addLayout(self.rows_layout)
        layout.addStretch()

        root = QVBoxLayout()
        root.addWidget(self.container)
        self.setLayout(root)

        self.drag_pos = None
        self._row_widgets = []
        self._last_signature = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(2000)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

    def refresh_settings(self):
        cfg = settings.load()
        kw = cfg["kda_window"]
        self.resize(kw["width"], kw["height"])
        self._opacity = kw["opacity"]
        self.container.setStyleSheet(
            f"background: rgba(0,0,0,{int(self._opacity * 220)}); "
            "border-radius: 8px;"
        )

    def refresh(self):
        state = gsi_server.get_state()
        if not state:
            return

        table = kda_tracker.get_kda_table(state)

        sig = tuple(
            (r.get("slot", 0), r["kills"], r["deaths"], r["assists"])
            for r in table
        )
        if sig == self._last_signature:
            return
        self._last_signature = sig

        self._render(table)

    def _clear(self):
        for w in self._row_widgets:
            w.setParent(None)
            w.deleteLater()
        self._row_widgets.clear()

    def _render(self, table):
        self._clear()

        if not table:
            label = QLabel("Ожидание данных...")
            label.setStyleSheet("color: #777; font-size: 11px;")
            self.rows_layout.addWidget(label)
            self._row_widgets.append(label)
            return

        for i, entry in enumerate(table):
            rank_color = RANK_COLORS[i] if i < len(RANK_COLORS) else "#AAAAAA"
            self._add_row(i + 1, entry, rank_color)

    def _add_row(self, rank, e, rank_color):
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(4, 3, 4, 3)
        layout.setSpacing(6)

        rank_label = QLabel(f"#{rank}")
        rank_label.setStyleSheet(
            f"color: {rank_color}; font-weight: bold; font-size: 11px;"
        )
        rank_label.setFixedWidth(28)
        layout.addWidget(rank_label)

        hero_path = dota_images.hero_image_path(e["hero"])
        if hero_path:
            h_icon = QLabel()
            pix = QPixmap(hero_path).scaled(
                28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            h_icon.setPixmap(pix)
            h_icon.setFixedWidth(30)
            layout.addWidget(h_icon)

        name_label = QLabel(e["name"][:12])
        name_label.setStyleSheet("color: #DDD; font-size: 10px;")
        name_label.setFixedWidth(85)
        layout.addWidget(name_label)

        kda_label = QLabel(
            f'<span style="color: #2ECC71;">{e["kills"]}</span>'
            f' / '
            f'<span style="color: #E74C3C;">{e["deaths"]}</span>'
            f' / '
            f'<span style="color: #5DADE2;">{e["assists"]}</span>'
        )
        kda_label.setTextFormat(Qt.RichText)
        kda_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        kda_label.setFixedWidth(70)
        layout.addWidget(kda_label)

        score_label = QLabel(f'{e["score"]:.1f}')
        score_label.setStyleSheet(
            f"color: {rank_color}; font-size: 12px; font-weight: bold;"
        )
        score_label.setFixedWidth(45)
        layout.addWidget(score_label)

        trend = e.get("trend", "flat")
        if trend == "up":
            arrow, color = "▲", TREND_UP
        elif trend == "down":
            arrow, color = "▼", TREND_DOWN
        else:
            arrow, color = "—", TREND_FLAT

        trend_label = QLabel(arrow)
        trend_label.setStyleSheet(f"color: {color}; font-size: 14px;")
        trend_label.setFixedWidth(20)
        layout.addWidget(trend_label)

        layout.addStretch()
        self.rows_layout.addWidget(row)
        self._row_widgets.append(row)


def create_kda_window():
    return KDAWindow()