from pathlib import Path

def load_settings():
    settings_path = Path(__file__).parent / "setting.txt"
    settings = {}
    with open(settings_path) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, _, value = line.partition("=")
                settings[key.strip()] = value.strip().strip('"').strip("'")
    return settings

_s = load_settings()
API_KEY = _s.get("API_KEY", "")
BASE_URL = _s.get("BASE_URL", "https://api.openai.com/v1")
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"
