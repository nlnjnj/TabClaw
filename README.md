<img src="asset/logo_rmbg.png" alt="TabClaw" height="80" />

**Table Intelligence Agent** — Upload CSVs or Excel files and talk to your data. TabClaw runs a full ReAct agent loop with planning, multi-agent parallel analysis, self-learning skills, and persistent memory — all in a local web UI with no external services required beyond an LLM API.

---

## Features

| Feature | Description |
|---|---|
| **ReAct Agent Loop** | Iterative Thought → Tool → Observation loop; automatically calls the right built-in skill |
| **Plan Mode** | LLM generates a step-by-step plan; user reviews and edits before execution |
| **Self-check (Reflection)** | After plan execution, agent verifies its own output and fills gaps |
| **Multi-Agent** | ≥ 2 tables + comparison keywords → parallel specialist agents per table, then an aggregator with `[CONSENSUS]` / `[UNCERTAIN]` markers |
| **Skill Learning** | After non-trivial tasks (≥ 3 tool calls), agent automatically distils a reusable custom skill from the interaction |
| **Intent Clarification** | Detects ambiguous requests and offers 2–4 option chips before executing |
| **Persistent Memory** | Learns user preferences and domain knowledge across sessions |
| **16 Built-in Skills** | filter, aggregate, sort, merge, pivot, add_column, describe_stats, correlation, value_counts, and more |
| **Custom Skills** | Add prompt-mode or sandboxed Python-code skills via the UI |
| **Code Tool** | Optional Python sandbox (AST-checked) for free-form pandas operations |
| **Light / Dark Mode** | One-click theme toggle, preference saved to localStorage |
| **Demo Mode** | One-click scenario runner with pre-loaded datasets and guided queries |

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/your-username/TabClaw.git
cd TabClaw
```

### 2. Configure API

```bash
cp setting.txt.example setting.txt
# Edit setting.txt and fill in your API_KEY and BASE_URL
```

> `setting.txt` is listed in `.gitignore` and will never be committed.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run

```bash
bash run.sh
# or directly:
python -m uvicorn app:app --host 0.0.0.0 --port 8022 --reload
```

Open **http://localhost:8022** in your browser.

---

## Configuration

All configuration lives in `setting.txt` (copied from `setting.txt.example`):

```ini
API_KEY=your_api_key_here
BASE_URL=https://api.openai.com/v1
```

The model is set in `config.py`:

```python
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"
```

TabClaw uses the **OpenAI-compatible API format**, so it works with any provider that supports it:

| Provider | BASE_URL |
|---|---|
| OpenAI | `https://api.openai.com/v1` |
| DeepSeek | `https://api.deepseek.com/v1` |
| SiliconFlow | `https://api.siliconflow.cn/v1` |
| Ollama (local) | `http://localhost:11434/v1` |

---

## Project Structure

```
TabClaw/
├── app.py                  # FastAPI application, all API endpoints
├── config.py               # Loads API_KEY / BASE_URL from setting.txt
├── setting.txt.example     # Config template (copy to setting.txt)
├── requirements.txt
├── run.sh                  # One-command startup script
│
├── agent/
│   ├── executor.py         # ReAct agent loop (execute / execute_plan)
│   ├── planner.py          # Plan generation + intent clarification
│   ├── multi_agent.py      # Parallel per-table agents + aggregator
│   ├── skill_distiller.py  # Post-task skill extraction
│   ├── memory.py           # Persistent user memory (JSON)
│   └── llm.py              # Async OpenAI-compatible LLM client
│
├── skills/
│   ├── registry.py         # Built-in + custom skill registry
│   ├── builtin.py          # 16 built-in pandas skills
│   └── code_skill.py       # AST-checked Python sandbox
│
├── static/
│   ├── index.html          # Single-page UI
│   ├── app.js              # Frontend state, streaming, rendering
│   └── style.css           # Dark/light theme, all component styles
│
├── examples/               # Demo CSV datasets
│   ├── sales_2023.csv
│   ├── employees.csv
│   ├── products.csv
│   ├── orders.csv
│   └── survey_nps.csv
│
├── data/                   # Runtime state (gitignored)
│   ├── memory.json         # User memory (auto-created)
│   └── custom_skills.json  # Saved custom skills (auto-created)
│
└── asset/
    └── logo_rmbg.png
```

---

## Architecture

```
Browser (SSE stream)
      │
      ▼
FastAPI (app.py)
      │
      ├─ /api/clarify ──────► Planner.check_clarification()
      ├─ /api/generate-plan ► Planner.generate()
      │
      ├─ /api/chat ─────────► AgentExecutor.execute()       ─┐
      │                    └► MultiAgentExecutor.execute_multi() ─┐ parallel
      │                                                    per-table agents
      └─ /api/execute-plan ► AgentExecutor.execute_plan()
                                    │
                          ┌─────────┴──────────┐
                          ▼                    ▼
                   ReAct loop           SkillDistiller
                (tool calls via         (post-task skill
                 SkillRegistry)          extraction)
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
          Built-in skills    Custom skills
          (pandas ops)       (prompt / code)
```

**Streaming protocol**: All agent responses use **Server-Sent Events (SSE)**. The frontend handles typed events:

| Event type | Meaning |
|---|---|
| `text_chunk` | Streaming LLM text |
| `tool_call` / `tool_result` | Skill invocation |
| `table` | New result table created |
| `step_start` / `step_done` | Plan step progress |
| `reflect_start` / `reflect_done` | Self-check pass |
| `agent_pool_start` / `agent_start` / `agent_done` | Multi-agent lifecycle |
| `aggregate_start` | Aggregator phase |
| `skill_learned` | New skill auto-saved |
| `final_text` | Complete response |

---

## Security Notes

- **`setting.txt` is gitignored** — never commit your API key.
- The Python sandbox (`code_skill.py`) uses AST inspection to block dangerous imports (`os`, `sys`, `subprocess`, network/file-system modules). Only whitelisted libraries (`pandas`, `numpy`, `math`, `re`, etc.) are permitted.
- The demo file loader (`/api/demo/load`) validates filenames to prevent path traversal.
- This is a **single-user local application**. It has no authentication layer and is not designed for multi-user or public internet deployment without additional hardening.

---

## License

MIT
