from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QSlider, QPushButton, QSpinBox, QGroupBox, QFormLayout,
    QLineEdit
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

import settings
import tts


class MenuWindow(QWidget):
    toggle_overlay = pyqtSignal(bool)
    toggle_purchase = pyqtSignal(bool)
    toggle_kda = pyqtSignal(bool)
    resize_overlay = pyqtSignal(int, int)
    resize_purchase = pyqtSignal(int, int)
    resize_kda = pyqtSignal(int, int)
    apply_all = pyqtSignal(dict)
    hotkeys_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dota Coach — Меню")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setGeometry(500, 100, 500, 820)

        self.setStyleSheet("""
            QWidget {
                background: #181818;
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
            QPushButton:hover { background: #5dade2; }
            QPushButton:pressed { background: #2874a6; }
            QPushButton#danger { background: #e74c3c; }
            QPushButton#danger:hover { background: #ec7063; }
            QPushButton#success { background: #27ae60; }
            QPushButton#success:hover { background: #2ecc71; }
            QLineEdit {
                background: #2a2a2a;
                color: #FFD700;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 4px 6px;
                font-weight: bold;
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

        title = QLabel("🎮 Dota Coach — Меню")
        title.setFont(QFont("Consolas", 14, QFont.Bold))
        title.setStyleSheet("color: #FFD700; padding: 6px;")
        root.addWidget(title)

        hint = QLabel("Нажми Del (или свою клавишу) — открыть / закрыть меню")
        hint.setStyleSheet("color: #888; font-size: 10px; padding-bottom: 6px;")
        root.addWidget(hint)

        # ── Оверлей подсказок ──
        ov_group = QGroupBox("Окно подсказок (COACH)")
        ov_layout = QFormLayout()

        self.cb_overlay = QCheckBox("Показывать")
        self.cb_overlay.setChecked(cfg["overlay"]["enabled"])
        self.cb_overlay.stateChanged.connect(self._quick_toggle)
        ov_layout.addRow(self.cb_overlay)

        self.sp_overlay_w = self._make_spin(cfg["overlay"]["width"], 280, 900)
        ov_layout.addRow("Ширина:", self.sp_overlay_w)

        self.sp_overlay_h = self._make_spin(cfg["overlay"]["height"], 200, 1000)
        ov_layout.addRow("Высота:", self.sp_overlay_h)

        self.sl_overlay_op = QSlider(Qt.Horizontal)
        self.sl_overlay_op.setRange(30, 100)
        self.sl_overlay_op.setValue(int(cfg["overlay"]["opacity"] * 100))
        ov_layout.addRow("Прозрачность:", self.sl_overlay_op)

        self.sp_overlay_font = self._make_spin(cfg["overlay"]["font_size"], 8, 18)
        ov_layout.addRow("Шрифт:", self.sp_overlay_font)

        ov_group.setLayout(ov_layout)
        root.addWidget(ov_group)

        # ── Лог покупок ──
        pur_group = QGroupBox("Окно лога покупок")
        pur_layout = QFormLayout()

        self.cb_purchase = QCheckBox("Показывать")
        self.cb_purchase.setChecked(cfg["purchase_window"]["enabled"])
        self.cb_purchase.stateChanged.connect(self._quick_toggle)
        pur_layout.addRow(self.cb_purchase)

        self.sp_pur_w = self._make_spin(cfg["purchase_window"]["width"], 300, 900)
        pur_layout.addRow("Ширина:", self.sp_pur_w)

        self.sp_pur_h = self._make_spin(cfg["purchase_window"]["height"], 300, 1000)
        pur_layout.addRow("Высота:", self.sp_pur_h)

        self.sl_pur_op = QSlider(Qt.Horizontal)
        self.sl_pur_op.setRange(30, 100)
        self.sl_pur_op.setValue(int(cfg["purchase_window"]["opacity"] * 100))
        pur_layout.addRow("Прозрачность:", self.sl_pur_op)

        pur_group.setLayout(pur_layout)
        root.addWidget(pur_group)

        # ── KDA ──
        kda_group = QGroupBox("Окно KDA")
        kda_layout = QFormLayout()

        self.cb_kda = QCheckBox("Показывать")
        self.cb_kda.setChecked(cfg["kda_window"]["enabled"])
        self.cb_kda.stateChanged.connect(self._quick_toggle)
        kda_layout.addRow(self.cb_kda)

        self.sp_kda_w = self._make_spin(cfg["kda_window"]["width"], 300, 900)
        kda_layout.addRow("Ширина:", self.sp_kda_w)

        self.sp_kda_h = self._make_spin(cfg["kda_window"]["height"], 200, 1000)
        kda_layout.addRow("Высота:", self.sp_kda_h)

        self.sl_kda_op = QSlider(Qt.Horizontal)
        self.sl_kda_op.setRange(30, 100)
        self.sl_kda_op.setValue(int(cfg["kda_window"]["opacity"] * 100))
        kda_layout.addRow("Прозрачность:", self.sl_kda_op)

        kda_group.setLayout(kda_layout)
        root.addWidget(kda_group)

        # ── ХОТКЕИ ──
        hk_group = QGroupBox("Хоткеи (глобальные)")
        hk_layout = QFormLayout()

        self.ed_menu_key = QLineEdit(cfg["hotkeys"].get("menu_key", "delete"))
        hk_layout.addRow("Меню:", self.ed_menu_key)

        self.ed_overlay_key = QLineEdit(cfg["hotkeys"].get("overlay_key", "f5"))
        hk_layout.addRow("Оверлей:", self.ed_overlay_key)

        self.ed_purchase_key = QLineEdit(cfg["hotkeys"].get("purchase_key", "f6"))
        hk_layout.addRow("Лог покупок:", self.ed_purchase_key)

        self.ed_kda_key = QLineEdit(cfg["hotkeys"].get("kda_key", "f7"))
        hk_layout.addRow("KDA:", self.ed_kda_key)

        hint_hk = QLabel(
            "Примеры: delete, insert, home, end, f8, ctrl+shift+d"
        )
        hint_hk.setStyleSheet("color: #888; font-size: 9px;")
        hk_layout.addRow(hint_hk)

        btn_hk = QPushButton("Применить хоткеи")
        btn_hk.setObjectName("success")
        btn_hk.clicked.connect(self._apply_hotkeys)
        hk_layout.addRow(btn_hk)

        hk_group.setLayout(hk_layout)
        root.addWidget(hk_group)

        # ── Блоки ──
        blocks_group = QGroupBox("Что показывать в оверлее")
        blocks_layout = QVBoxLayout()

        self.cb_timings = QCheckBox("Тайминги предметов")
        self.cb_timings.setChecked(cfg["blocks"]["timings"])
        blocks_layout.addWidget(self.cb_timings)

        self.cb_threats = QCheckBox("Угрозы врага")
        self.cb_threats.setChecked(cfg["blocks"]["threats"])
        blocks_layout.addWidget(self.cb_threats)

        self.cb_general = QCheckBox("Общие советы")
        self.cb_general.setChecked(cfg["blocks"]["general"])
        blocks_layout.addWidget(self.cb_general)

        blocks_group.setLayout(blocks_layout)
        root.addWidget(blocks_group)

        # ── Озвучка ──
        tts_group = QGroupBox("Озвучка (TTS)")
        tts_layout = QFormLayout()

        self.cb_tts = QCheckBox("Включить")
        self.cb_tts.setChecked(cfg["tts"]["enabled"])
        tts_layout.addRow(self.cb_tts)

        self.sl_tts_vol = QSlider(Qt.Horizontal)
        self.sl_tts_vol.setRange(0, 100)
        self.sl_tts_vol.setValue(int(cfg["tts"]["volume"] * 100))
        tts_layout.addRow("Громкость:", self.sl_tts_vol)

        self.sp_tts_rate = self._make_spin(cfg["tts"]["rate"], 100, 300)
        tts_layout.addRow("Скорость:", self.sp_tts_rate)

        tts_group.setLayout(tts_layout)
        root.addWidget(tts_group)

        # ── Кнопки ──
        btn_row = QHBoxLayout()

        btn_test = QPushButton("Проверить голос")
        btn_test.clicked.connect(self._test_voice)
        btn_row.addWidget(btn_test)

        btn_apply = QPushButton("Применить")
        btn_apply.clicked.connect(self._apply)
        btn_row.addWidget(btn_apply)

        btn_reset = QPushButton("Сброс")
        btn_reset.setObjectName("danger")
        btn_reset.clicked.connect(self._reset)
        btn_row.addWidget(btn_reset)

        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.hide)
        btn_row.addWidget(btn_close)

        root.addLayout(btn_row)

        self._sync_spins()

    # ─────────────────────────────────────
    def _make_spin(self, value, min_v, max_v):
        sp = QSpinBox()
        sp.setRange(min_v, max_v)
        sp.setValue(value)
        return sp

    def _sync_spins(self):
        cfg = settings.load()
        self.sp_overlay_w.setValue(cfg["overlay"]["width"])
        self.sp_overlay_h.setValue(cfg["overlay"]["height"])
        self.sp_pur_w.setValue(cfg["purchase_window"]["width"])
        self.sp_pur_h.setValue(cfg["purchase_window"]["height"])
        self.sp_kda_w.setValue(cfg["kda_window"]["width"])
        self.sp_kda_h.setValue(cfg["kda_window"]["height"])

        self.ed_menu_key.setText(cfg["hotkeys"].get("menu_key", "delete"))
        self.ed_overlay_key.setText(cfg["hotkeys"].get("overlay_key", "f5"))
        self.ed_purchase_key.setText(cfg["hotkeys"].get("purchase_key", "f6"))
        self.ed_kda_key.setText(cfg["hotkeys"].get("kda_key", "f7"))

    def _quick_toggle(self):
        self.toggle_overlay.emit(self.cb_overlay.isChecked())
        self.toggle_purchase.emit(self.cb_purchase.isChecked())
        self.toggle_kda.emit(self.cb_kda.isChecked())

        cfg = settings.load()
        cfg["overlay"]["enabled"] = self.cb_overlay.isChecked()
        cfg["purchase_window"]["enabled"] = self.cb_purchase.isChecked()
        cfg["kda_window"]["enabled"] = self.cb_kda.isChecked()
        settings.save(cfg)

    def _test_voice(self):
        tts.say("Проверка голоса. Один, два, три.")

    def _apply_hotkeys(self):
        """Применить новые хоткеи без перезапуска."""
        cfg = settings.load()

        new_keys = {
            "menu_key": self.ed_menu_key.text().strip().lower(),
            "overlay_key": self.ed_overlay_key.text().strip().lower(),
            "purchase_key": self.ed_purchase_key.text().strip().lower(),
            "kda_key": self.ed_kda_key.text().strip().lower(),
        }

        cfg["hotkeys"] = new_keys
        settings.save(cfg)

        self.hotkeys_changed.emit(new_keys)
        print(f"[menu] хоткеи обновлены: {new_keys}")

    def _apply(self):
        cfg = settings.load()

        cfg["overlay"]["enabled"] = self.cb_overlay.isChecked()
        cfg["overlay"]["width"] = self.sp_overlay_w.value()
        cfg["overlay"]["height"] = self.sp_overlay_h.value()
        cfg["overlay"]["opacity"] = self.sl_overlay_op.value() / 100
        cfg["overlay"]["font_size"] = self.sp_overlay_font.value()

        cfg["purchase_window"]["enabled"] = self.cb_purchase.isChecked()
        cfg["purchase_window"]["width"] = self.sp_pur_w.value()
        cfg["purchase_window"]["height"] = self.sp_pur_h.value()
        cfg["purchase_window"]["opacity"] = self.sl_pur_op.value() / 100

        cfg["kda_window"]["enabled"] = self.cb_kda.isChecked()
        cfg["kda_window"]["width"] = self.sp_kda_w.value()
        cfg["kda_window"]["height"] = self.sp_kda_h.value()
        cfg["kda_window"]["opacity"] = self.sl_kda_op.value() / 100

        cfg["blocks"]["timings"] = self.cb_timings.isChecked()
        cfg["blocks"]["threats"] = self.cb_threats.isChecked()
        cfg["blocks"]["general"] = self.cb_general.isChecked()

        cfg["tts"]["enabled"] = self.cb_tts.isChecked()
        cfg["tts"]["volume"] = self.sl_tts_vol.value() / 100
        cfg["tts"]["rate"] = self.sp_tts_rate.value()

        settings.save(cfg)
        tts.set_enabled(cfg["tts"]["enabled"])

        self.toggle_overlay.emit(cfg["overlay"]["enabled"])
        self.toggle_purchase.emit(cfg["purchase_window"]["enabled"])
        self.toggle_kda.emit(cfg["kda_window"]["enabled"])

        self.resize_overlay.emit(cfg["overlay"]["width"], cfg["overlay"]["height"])
        self.resize_purchase.emit(cfg["purchase_window"]["width"], cfg["purchase_window"]["height"])
        self.resize_kda.emit(cfg["kda_window"]["width"], cfg["kda_window"]["height"])

        self.apply_all.emit(cfg)
        print("[menu] настройки применены")

    def _reset(self):
        from settings import DEFAULTS
        settings.save(DEFAULTS)
        print("[menu] настройки сброшены (перезапусти main.py)")