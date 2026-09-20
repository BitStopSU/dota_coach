import sys
import threading

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, Qt

import gsi_server
import settings
import match_logger
from overlay import create_overlay
from purchase_window import PurchaseWindow
from settings_window import SettingsWindow
from kda_window import KDAWindow
from menu_window import MenuWindow

# ── Глобальный хоткей через keyboard ──
try:
    import keyboard
    _KEYBOARD_OK = True
except ImportError:
    _KEYBOARD_OK = False
    print("[coach] keyboard не установлен — хоткеи не работают")
    print("[coach] установи: python -m pip install keyboard")


class HotkeyEmitter(QObject):
    """Излучает сигналы в главный поток Qt при нажатии хоткеев."""
    menu_pressed = pyqtSignal()
    overlay_pressed = pyqtSignal()
    purchase_pressed = pyqtSignal()
    kda_pressed = pyqtSignal()


def start_gsi():
    try:
        gsi_server.run_server()
    except Exception as e:
        print(f"[coach] ошибка GSI-сервера: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("[coach] Dota Coach запускается...")
    print("=" * 50)

    cfg = settings.load()
    print("[coach] настройки загружены")

    match_logger.log_event("SESSION", "Запуск Dota Coach")
    log_path = match_logger.get_log_path()
    print(f"[coach] лог сессии: {log_path}")

    print("[coach] запуск GSI-сервера на 127.0.0.1:3000")
    threading.Thread(target=start_gsi, daemon=True).start()

    print("[coach] запуск интерфейса...")
    app = QApplication(sys.argv)

    # ─────────────────────────────────────────
    #  Создание окон
    # ─────────────────────────────────────────
    overlay = create_overlay()
    purchases = PurchaseWindow()
    kda = KDAWindow()

    if cfg["overlay"]["enabled"]:
        overlay.show()
    if cfg["purchase_window"]["enabled"]:
        purchases.show()
    if cfg["kda_window"]["enabled"]:
        kda.show()

    # ─────────────────────────────────────────
    #  Меню
    # ─────────────────────────────────────────
    menu = MenuWindow()

    menu.toggle_overlay.connect(
        lambda v: overlay.show() if v else overlay.hide()
    )
    menu.toggle_purchase.connect(
        lambda v: purchases.show() if v else purchases.hide()
    )
    menu.toggle_kda.connect(
        lambda v: kda.show() if v else kda.hide()
    )

    menu.resize_overlay.connect(lambda w, h: overlay.resize(w, h))
    menu.resize_purchase.connect(lambda w, h: purchases.resize(w, h))
    menu.resize_kda.connect(lambda w, h: kda.resize(w, h))

    def on_apply_all(new_cfg):
        try:
            overlay.refresh_settings()
            purchases.refresh_settings()
            kda.refresh_settings()
        except Exception as e:
            print(f"[coach] ошибка применения: {e}")

    menu.apply_all.connect(on_apply_all)

    # ─────────────────────────────────────────
    #  Хоткеи
    # ─────────────────────────────────────────
    hotkey_emitter = HotkeyEmitter()

    def toggle_menu():
        if menu.isVisible():
            menu.hide()
        else:
            menu.show()
            menu.raise_()
            menu.activateWindow()
            menu._sync_spins()

    def toggle_window(window):
        """Показать если скрыто, скрыть если показано."""
        if window.isVisible():
            window.hide()
        else:
            window.show()
            window.raise_()
            window.activateWindow()

    def toggle_overlay_win():
        toggle_window(overlay)

    def toggle_purchase_win():
        toggle_window(purchases)

    def toggle_kda_win():
        toggle_window(kda)

    hotkey_emitter.menu_pressed.connect(toggle_menu, Qt.QueuedConnection)
    hotkey_emitter.overlay_pressed.connect(toggle_overlay_win, Qt.QueuedConnection)
    hotkey_emitter.purchase_pressed.connect(toggle_purchase_win, Qt.QueuedConnection)
    hotkey_emitter.kda_pressed.connect(toggle_kda_win, Qt.QueuedConnection)

    # Регистрация глобальных хоткеев
    if _KEYBOARD_OK:
        try:
            menu_key = cfg["hotkeys"].get("menu_key", "delete")
            keyboard.add_hotkey(
                menu_key,
                lambda: hotkey_emitter.menu_pressed.emit()
            )
            print(f"[coach] хоткей '{menu_key}' → меню")

            overlay_key = cfg["hotkeys"].get("overlay_key", "f5")
            keyboard.add_hotkey(
                overlay_key,
                lambda: hotkey_emitter.overlay_pressed.emit()
            )
            print(f"[coach] хоткей '{overlay_key}' → оверлей подсказок")

            purchase_key = cfg["hotkeys"].get("purchase_key", "f6")
            keyboard.add_hotkey(
                purchase_key,
                lambda: hotkey_emitter.purchase_pressed.emit()
            )
            print(f"[coach] хоткей '{purchase_key}' → лог покупок")

            kda_key = cfg["hotkeys"].get("kda_key", "f7")
            keyboard.add_hotkey(
                kda_key,
                lambda: hotkey_emitter.kda_pressed.emit()
            )
            print(f"[coach] хоткей '{kda_key}' → KDA")

        except Exception as e:
            print(f"[coach] ошибка регистрации хоткея: {e}")
    else:
        print("[coach] хоткеи недоступны без библиотеки keyboard")

    # ─────────────────────────────────────────
    #  Старое окно настроек (двойной клик по оверлею → меню)
    # ─────────────────────────────────────────
    def open_menu_from_overlay():
        toggle_menu()

    overlay.open_settings_callback = open_menu_from_overlay

    # ─────────────────────────────────────────
    #  Готово
    # ─────────────────────────────────────────
    print("[coach] готов к работе.")
    print("[coach] Del = меню | F5 = оверлей | F6 = покупки | F7 = KDA")
    print("[coach] Нажми Ctrl+C для выхода.")

    try:
        exit_code = app.exec_()
    except KeyboardInterrupt:
        print("\n[coach] остановка")
        exit_code = 0

    match_logger.log_event("SESSION", "Завершение Dota Coach")
    sys.exit(exit_code)