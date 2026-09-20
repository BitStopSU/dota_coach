from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QSlider, QPushButton, QSpinBox, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt

import settings
import tts


class SettingsWindow(QWidget):
    def __init__(self, on_apply=None):
        super().__init__()
        self.on_apply = on_apply

        self.setWindowTitle("Dota Coach — Настройки (старое окно)")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setGeometry(200, 200, 420, 620)

        self.setStyleSheet("""
            QWidget {
                background: #1e1e1e;
                color: #EEEEEE;
                font-family: Consolas;
                font-size: 11px;
            }
            QGroupBox {
                border: 1px solid #444;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #FFD700;
                left: 10px;
                padding: 0 4px;
            }
            QPushButton {
                background: #3498db;
                color: white;
                border-radius: 4px;
                padding: 6px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #5dade2;
            }
            QPushButton:pressed {
                background: #2874a6;
            }
            QCheckBox {
                padding: 4px 0;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #333;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #FFD700;
                width: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
        """)

        cfg = settings.load()

        root = QVBoxLayout(self)
        root.setSpacing(8)

        # ── Блоки оверлея ──
        blocks_group = QGroupBox("Что показывать в оверлее")
        blocks_layout = QVBoxLayout()

        self.cb_timings = QCheckBox("Тайминги предметов")
        self.cb_timings.setChecked(cfg["blocks"]["timings"])
        blocks_layout.addWidget(self.cb_timings)

        self.cb_threats = QCheckBox("Угрозы врага и контр-предметы")
        self.cb_threats.setChecked(cfg["blocks"]["threats"])
        blocks_layout.addWidget(self.cb_threats)

        self.cb_general = QCheckBox("Общие советы")
        self.cb_general.setChecked(cfg["blocks"]["general"])
        blocks_layout.addWidget(self.cb_general)

        self.cb_purchase = QCheckBox("Окно лога покупок")
        self.cb_purchase.setChecked(cfg["purchase_window"]["enabled"])
        blocks_layout.addWidget(self.cb_purchase)

        blocks_group.setLayout(blocks_layout)
        root.addWidget(blocks_group)

        # ── Внешний вид ──
        view_group = QGroupBox("Внешний вид оверлея")
        view_layout = QFormLayout()

        self.slider_opacity = QSlider(Qt.Horizontal)
        self.slider_opacity.setRange(30, 100)
        self.slider_opacity.setValue(int(cfg["overlay"]["opacity"] * 100))
        view_layout.addRow("Прозрачность:", self.slider_opacity)

        self.spin_font = QSpinBox()
        self.spin_font.setRange(8, 18)
        self.spin_font.setValue(cfg["overlay"]["font_size"])
        view_layout.addRow("Размер шрифта:", self.spin_font)

        self.spin_width = QSpinBox()
        self.spin_width.setRange(280, 900)
        self.spin_width.setValue(cfg["overlay"]["width"])
        view_layout.addRow("Ширина окна:", self.spin_width)

        self.spin_height = QSpinBox()
        self.spin_height.setRange(200, 1000)
        self.spin_height.setValue(cfg["overlay"]["height"])
        view_layout.addRow("Высота окна:", self.spin_height)

        view_group.setLayout(view_layout)
        root.addWidget(view_group)

        # ── Озвучка ──
        tts_group = QGroupBox("Озвучка (TTS)")
        tts_layout = QFormLayout()

        self.cb_tts = QCheckBox("Включить озвучку")
        self.cb_tts.setChecked(cfg["tts"]["enabled"])
        tts_layout.addRow(self.cb_tts)

        self.slider_volume = QSlider(Qt.Horizontal)
        self.slider_volume.setRange(0, 100)
        self.slider_volume.setValue(int(cfg["tts"]["volume"] * 100))
        tts_layout.addRow("Громкость:", self.slider_volume)

        self.spin_rate = QSpinBox()
        self.spin_rate.setRange(100, 300)
        self.spin_rate.setValue(cfg["tts"]["rate"])
        tts_layout.addRow("Скорость:", self.spin_rate)

        tts_group.setLayout(tts_layout)
        root.addWidget(tts_group)

        # ── Кнопки ──
        btn_row = QHBoxLayout()

        btn_test = QPushButton("Проверить голос")
        btn_test.clicked.connect(self.test_voice)
        btn_row.addWidget(btn_test)

        btn_save = QPushButton("Сохранить")
        btn_save.clicked.connect(self.save_settings)
        btn_row.addWidget(btn_save)

        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.close)
        btn_row.addWidget(btn_close)

        root.addLayout(btn_row)

    def test_voice(self):
        """Озвучить тестовую фразу."""
        tts.say("Проверка голоса. Один, два, три.")

    def save_settings(self):
        """Сохранить настройки в config.json и применить."""
        cfg = settings.load()

        # Блоки
        cfg["blocks"]["timings"] = self.cb_timings.isChecked()
        cfg["blocks"]["threats"] = self.cb_threats.isChecked()
        cfg["blocks"]["general"] = self.cb_general.isChecked()
        cfg["purchase_window"]["enabled"] = self.cb_purchase.isChecked()

        # Внешний вид
        cfg["overlay"]["opacity"] = self.slider_opacity.value() / 100
        cfg["overlay"]["font_size"] = self.spin_font.value()
        cfg["overlay"]["width"] = self.spin_width.value()
        cfg["overlay"]["height"] = self.spin_height.value()

        # Озвучка
        cfg["tts"]["enabled"] = self.cb_tts.isChecked()
        cfg["tts"]["volume"] = self.slider_volume.value() / 100
        cfg["tts"]["rate"] = self.spin_rate.value()

        settings.save(cfg)

        # Применить к TTS сразу
        tts.set_enabled(cfg["tts"]["enabled"])

        # Уведомить main.py
        if self.on_apply:
            self.on_apply(cfg)

        print("[settings] сохранено в config.json")