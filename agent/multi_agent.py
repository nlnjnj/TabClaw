"""Multi-agent parallel execution for multi-table analysis.

Each table gets a specialist agent that runs independently (in parallel).
An aggregator then synthesises all findings and marks:
  [CONSENSUS]  — conclusions most/all agents agree on  (high confidence)
  [UNCERTAIN]  — conflicting or caveat-heavy findings  (low confidence)
"""
import asyncio
from typing import AsyncGenerator, Dict, List

from agent.executor import AgentExecutor

_MULTI_AGENT_KEYWORDS = [
    # Chinese
    "对比", "比较", "分别", "各表", "综合", "横向", "差异", "相同", "不同",
    "两张", "三张", "多张", "所有表", "每张", "各个",
    # English
    "compare", "contrast", "overview", "across", "each table", "all tables",
    "differences", "similarities", "side by side",
]


class MultiAgentExecutor(AgentExecutor):
    """Specialist-per-table agents running in parallel, with an aggregator."""

    def should_activate(self, message: str, tables: Dict) -> bool:
        if len(tables) < 2:
            return False
        msg_lower = message.lower()
        return any(kw in msg_lower for kw in _MULTI_AGENT_KEYWORDS)

    async def execute_multi(
        self,
        message: str,
        tables: Dict,
        history: List,
        result_tables_store: Dict,
        code_tool: bool = False,
    ) -> AsyncGenerator:
        tools = self.skills.get_tool_definitions(code_tool=code_tool)

        # Announce the agent pool
        agents_info = [
            {"id": tid, "table_name": t["name"]}
            for tid, t in tables.items()
        ]
        yield {"type": "agent_pool_start", "agents": agents_info}

        # ── Parallel per-table agents ─────────────────────────────────────────
        _DONE = object()
        queue: asyncio.Queue = asyncio.Queue()

        async def run_agent(tid: str, table: Dict) -> str:
            try:
                await queue.put({
                    "type": "agent_start",
                    "agent_id": tid,
                    "table_name": table["name"],
                })
                # Scoped system prompt — shows only this table
                scoped_system = self._system_prompt({tid: table})
                msgs = [{"role": "system", "content": scoped_system}]
                msgs.extend(history[-6:])
                msgs.append({
                    "role": "user",
                    "content": (
                        f"You are a specialist analyst assigned to the table "
                        f"'{table['name']}'.\n"
                        f"User request: {message}\n\n"
                        "Analyse this table thoroughly. Always call table_info "
                        "first. Use specific numbers and column names."
                    ),
                })

                conclusion = ""
                # Use shared result_tables_store so created tables persist
                async for event in self._agent_stream(
                    msgs, tools, result_tables_store, result_tables_store
                ):
                    await queue.put({**event, "agent_id": tid})
                    if event["type"] == "final_text":
                        conclusion = event["content"]

                await queue.put({
                    "type": "agent_done",
                    "agent_id": tid,
                    "conclusion": conclusion,
                })
                return conclusion
            except Exception as exc:
                conclusion = f"(Agent error: {exc})"
                await queue.put({
                    "type": "agent_done",
                    "agent_id": tid,
                    "conclusion": conclusion,
                    "error": True,
                })
                return conclusion
            finally:
                await queue.put(_DONE)

        tasks = [
            asyncio.create_task(run_agent(tid, t))
            for tid, t in tables.items()
        ]

        done_count = 0
        n = len(tables)
        while done_count < n:
            event = await queue.get()
            if event is _DONE:
                done_count += 1
            else:
                yield event

        await asyncio.gather(*tasks, return_exceptions=True)
        conclusions: Dict[str, str] = {}
        for tid, task in zip(tables.keys(), tasks):
            try:
                conclusions[tid] = task.result() or ""
            except Exception:
                conclusions[tid] = ""

        # ── Aggregation with uncertainty markers ──────────────────────────────
        yield {"type": "aggregate_start"}
        async for event in self._run_aggregator(message, conclusions, tables):
            yield event

        await self._try_update_memory(message, tables)

    # ------------------------------------------------------------------
    # Aggregator
    # ------------------------------------------------------------------

    async def _run_aggregator(
        self,
        message: str,
        conclusions: Dict[str, str],
        tables: Dict,
    ) -> AsyncGenerator:
        parts = [
            f"**'{tables.get(tid, {}).get('name', tid)}' analyst findings:**\n{c}"
            for tid, c in conclusions.items()
            if c
        ]
        conclusions_text = "\n\n---\n\n".join(parts) or "(no findings)"

        prompt = f"""You are synthesising findings from {len(conclusions)} specialist analysts who each examined one table.

Original user request: {message}

Individual analyst findings:
{conclusions_text}

Instructions:
- Prefix conclusions agreed on by all or most analysts with **[CONSENSUS]**
- Prefix uncertain, conflicting, or caveat-heavy findings with **[UNCERTAIN]**
- Provide cross-table insights — comparisons, correlations, or patterns that span multiple tables
- Do NOT simply repeat each analyst; synthesise and compare
- End with ## ✅ 最终结论 with 3–6 bullet points"""

        full_content = ""
        try:
            async for chunk in self.llm.stream_chat(
                [{"role": "user", "content": prompt}]
            ):
                choice = chunk.choices[0] if chunk.choices else None
                if not choice:
                    continue
                delta = choice.delta
                if delta.content:
                    full_content += delta.content
                    yield {"type": "text_chunk", "content": delta.content}
                if choice.finish_reason in ("stop", "end_turn"):
                    break
        except Exception as exc:
            yield {"type": "error", "content": f"Aggregation error: {exc}"}
            return

        yield {"type": "final_text", "content": full_content}
