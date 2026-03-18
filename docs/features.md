# ✨ Features

## Agent Loop

TabClaw runs a **ReAct loop** (Reason → Act → Observe) powered by an OpenAI-compatible LLM. On every turn the agent decides which tool to call, executes it, reads the result, and iterates — up to 12 times — until it produces a final answer.

## Plan Mode

Toggle **Plan Mode** in the input toolbar. Instead of executing immediately, the LLM drafts a step-by-step plan. You can **add, delete, or rewrite any step** before hitting Execute. After execution, a lightweight **self-check pass** verifies the original request was fully addressed.

## Intent Clarification

Before executing any request, TabClaw silently calls a clarification check. If the request is genuinely ambiguous, an interactive card appears with **2–4 option chips** (plus a free-text field) for you to specify intent. Unambiguous requests pass through instantly with no delay.

## Multi-Agent (Parallel Analysis)

When **two or more tables** are uploaded and the query contains comparison keywords (`compare`, `对比`, `各表`, `differences`, etc.), TabClaw automatically spawns one **specialist agent per table** running in parallel. Each agent only sees its own table. An **Aggregator** then synthesises all findings and marks:

- **[CONSENSUS]** — conclusions most/all agents agree on
- **[UNCERTAIN]** — conflicting or caveat-heavy findings

## Skill Learning

After non-trivial tasks (≥ 3 tool calls), TabClaw reviews what it did and asks itself: *"Is there a reusable skill here?"* If yes, it automatically creates a new **custom skill** — either Python code or a prompt template — and saves it for future sessions. A 🧠 badge appears in the chat when a skill is learned.

## Persistent Memory

TabClaw extracts preferences and domain facts from every conversation and stores them in `data/memory.json`. On the next session they are injected into the system prompt, so the agent already knows your preferences. You can view, edit, or clear memory from the **Memory** sidebar panel.

## Custom Skills

Beyond the 16 built-in skills, you can define your own:

- **Prompt mode** — write a system prompt template; the LLM executes it with a 30-row table preview as context
- **Code mode** — write sandboxed Python (pandas/numpy); runs in the same AST-checked sandbox as Code Tool

See [Skills Reference](skills.md) for the full list of built-in skills and sandbox rules.

## Code Tool

Enable **Code Tool** in the toolbar to let the agent write and run arbitrary pandas code in a sandboxed Python environment. Useful for complex transformations that no single built-in skill covers.

## Light / Dark Mode

Click the ☀️ / 🌙 button in the header. Preference is saved to `localStorage` and restored on next visit.

## Demo Mode

Click **一键体验** to load a pre-built scenario (sales analysis, HR insights, order–product join, NPS survey). The app auto-loads the dataset and runs through a guided sequence of queries.
