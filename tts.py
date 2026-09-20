import threading
import time

try:
    import pyttsx3
    _TTS_AVAILABLE = True
except ImportError:
    _TTS_AVAILABLE = False
    print("[tts] pyttsx3 не установлен — озвучка отключена")


class TTS:
    def __init__(self, enabled=True, volume=0.9, rate=180):
        self.enabled = enabled and _TTS_AVAILABLE
        self.engine = None
        self.lock = threading.Lock()
        self.last_spoken = {}  # {key: timestamp}

        if not self.enabled:
            return

        try:
            self.engine = pyttsx3.init()

            # Ищем русский голос
            voices = self.engine.getProperty("voices")
            for v in voices:
                vid = (v.id or "").lower()
                vname = (v.name or "").lower()
                if "ru" in vid or "russian" in vname or "irina" in vname:
                    self.engine.setProperty("voice", v.id)
                    break

            self.engine.setProperty("rate", rate)
            self.engine.setProperty("volume", volume)
        except Exception as e:
            print(f"[tts] ошибка инициализации: {e}")
            self.enabled = False

    def say(self, text, key=None, cooldown=30):
        """
        Озвучить текст.
        key: уникальный ключ события (например, 'rune_river').
             Одно и то же событие не повторяется чаще чем cooldown секунд.
        """
        if not self.enabled or not text:
            return

        now = time.time()
        if key:
            last = self.last_spoken.get(key, 0)
            if now - last < cooldown:
                return
            self.last_spoken[key] = now

        threading.Thread(target=self._speak, args=(text,), daemon=True).start()

    def _speak(self, text):
        try:
            with self.lock:
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception as e:
            print(f"[tts] ошибка речи: {e}")


# Глобальный экземпляр
_tts = TTS(enabled=True)


def say(text, key=None, cooldown=30):
    _tts.say(text, key=key, cooldown=cooldown)


def set_enabled(value):
    _tts.enabled = value and _TTS_AVAILABLE