"""
Обёртка над LLM. Сейчас поддерживает DeepSeek (через OpenAI SDK).
Легко расширяется на Gemini или Ollama.
"""

import settings

# OpenAI-совместимый SDK
try:
    from openai import OpenAI
    _OPENAI_OK = True
except ImportError:
    _OPENAI_OK = False
    print("[ai] библиотека openai не установлена")
    print("[ai] установи: python -m pip install openai")


_client = None
_client_key = None


def _get_client():
    """Создать/переиспользовать клиент OpenAI SDK для DeepSeek."""
    global _client, _client_key

    if not _OPENAI_OK:
        raise RuntimeError("Библиотека openai не установлена")

    cfg = settings.load()
    ai = cfg.get("ai", {})

    api_key = ai.get("deepseek_api_key", "").strip()
    base_url = ai.get("deepseek_base_url", "https://api.deepseek.com")

    if not api_key:
        raise RuntimeError(
            "Не задан API-ключ DeepSeek. Открой config.json и вставь "
            "ключ в поле ai.deepseek_api_key"
        )

    # Если клиент уже создан с тем же ключом — переиспользуем
    if _client is not None and _client_key == api_key:
        return _client

    _client = OpenAI(api_key=api_key, base_url=base_url)
    _client_key = api_key
    return _client


def ask(prompt, system=None, max_tokens=1500, temperature=0.7):
    """
    Отправить промпт в LLM и получить ответ.
    Возвращает строку ответа.
    """
    cfg = settings.load()
    ai = cfg.get("ai", {})
    model = ai.get("deepseek_model", "deepseek-chat")

    client = _get_client()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        text = resp.choices[0].message.content
        return text.strip() if text else ""
    except Exception as e:
        print(f"[ai] ошибка запроса: {e}")
        return f"❌ Ошибка запроса к ИИ: {e}"


def is_ready():
    """Проверить, есть ли ключ и SDK."""
    if not _OPENAI_OK:
        return False
    cfg = settings.load()
    key = cfg.get("ai", {}).get("deepseek_api_key", "").strip()
    return bool(key)