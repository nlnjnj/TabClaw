# 🏗️ Architecture

## Project Structure

```
TabClaw/
├── app.py                  # FastAPI app, all API endpoints
├── config.py               # Loads API_KEY / BASE_URL from setting.txt
├── setting.txt.example     # Config template — copy to setting.txt
├── requirements.txt
├── run.sh
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
│   ├── registry.py         # Built-in + custom skill registry & tool defs
│   ├── builtin.py          # 16 built-in pandas skills
│   └── code_skill.py       # AST-checked Python sandbox
│
├── static/
│   ├── index.html          # Single-page UI
│   ├── app.js              # Frontend state, streaming, rendering
│   └── style.css           # Dark/light theme, all component styles
│
├── examples/               # Demo CSV datasets
├── docs/                   # This documentation
├── asset/                  # Logo
└── data/                   # Runtime state (gitignored)
```

## System Design

```
Browser (SSE stream)
      │
      ▼
FastAPI (app.py)
      │
      ├─ POST /api/clarify ────► Planner.check_clarification()
      ├─ POST /api/generate-plan ► Planner.generate()
      │
      ├─ POST /api/chat ───────► AgentExecutor.execute()
      │                       └► MultiAgentExecutor.execute_multi()
      │                              ├─ Agent (table 1) ─┐ parallel
      │                              ├─ Agent (table 2) ─┤
      │                              └─ Aggregator ───────┘
      │
      └─ POST /api/execute-plan ► AgentExecutor.execute_plan()
                                        │
                              ┌─────────┴──────────┐
                              ▼                    ▼
                       ReAct loop           SkillDistiller
                    (tool calls via         (post-task skill
                     SkillRegistry)          extraction)
```

## SSE Event Reference

All agent responses stream via **Server-Sent Events**. The frontend (`app.js`) dispatches on `event.type`:

| Event | Description |
|---|---|
| `text_chunk` | Streaming LLM text delta |
| `tool_call` | Skill invoked — name + params |
| `tool_result` | Skill output text |
| `table` | New result table created |
| `step_start` / `step_done` | Plan step progress |
| `reflect_start` / `reflect_done` | Self-check pass |
| `agent_pool_start` | Multi-agent mode started |
| `agent_start` / `agent_done` | Per-table agent lifecycle |
| `aggregate_start` | Aggregator phase started |
| `skill_learned` | New custom skill auto-saved |
| `final_text` | Complete response content |
| `error` | Error from agent or skill |
