<img src="asset/logo_rmbg.png" alt="TabClaw" width="100%" />

**Table Intelligence Agent** — Upload CSVs or Excel files and talk to your data.

---

## Quick Start

```bash
git clone https://github.com/fishsure/TabClaw.git
cd TabClaw

# 1. Configure your API key
cp setting.txt.example setting.txt
# Edit setting.txt: fill in API_KEY and BASE_URL

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
bash run.sh
```

Open **http://localhost:8022** in your browser.

---

## Docs

| | |
|---|---|
| [✨ Features](docs/features.md) | Agent loop, plan mode, multi-agent, skill learning, memory… |
| [⚙️ Configuration](docs/configuration.md) | API providers, model selection, setting.txt reference |
| [🏗️ Architecture](docs/architecture.md) | System design, SSE streaming protocol, project structure |
| [🛠️ Skills Reference](docs/skills.md) | Built-in skills list, custom skills, Python sandbox |

---

## Security

`setting.txt` is listed in `.gitignore` and will **never** be committed.
See [Configuration](docs/configuration.md) for details.

---

## License

MIT
