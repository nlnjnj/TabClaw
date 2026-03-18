# ⚙️ Configuration

## setting.txt

Copy the example file and fill in your credentials:

```bash
cp setting.txt.example setting.txt
```

`setting.txt` is listed in `.gitignore` and will **never** be committed to git.

```ini
# Your LLM API key
API_KEY=your_api_key_here

# API base URL (OpenAI-compatible endpoint)
BASE_URL=https://api.openai.com/v1
```

## Supported Providers

TabClaw uses the **OpenAI-compatible API format** and works with any provider that supports it:

| Provider | BASE_URL |
|---|---|
| OpenAI | `https://api.openai.com/v1` |
| DeepSeek | `https://api.deepseek.com/v1` |
| SiliconFlow | `https://api.siliconflow.cn/v1` |
| Ollama (local) | `http://localhost:11434/v1` |
| Any OpenAI-compatible API | your endpoint |

## Model

The default model is set in `config.py`:

```python
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"
```

Change this to any model your provider supports, e.g. `gpt-4o`, `deepseek-chat`, `qwen2.5-72b-instruct`.

## Runtime Data

The following files are created automatically at runtime and are gitignored:

| File | Contents |
|---|---|
| `data/memory.json` | User memory (preferences, domain knowledge) |
| `data/custom_skills.json` | Custom skills saved from the UI or learned by the agent |
| `uploads/` | Temporarily uploaded files |
