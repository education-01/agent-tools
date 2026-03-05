# -*- coding: utf-8 -*-
"""
Agent Tools - AI 代理工具系统

参考实现:
- https://github.com/anomalyco/opencode/tree/main/packages/opencode/src/tool (OpenCode 工具实现)
- https://github.com/badlogic/pi-mono/tree/master/packages/coding-agent (pi-coding-agent)
- https://github.com/openai/openai-agents-python (OpenAI Agents SDK)

工具模块:
- filesystem: read, write, edit, glob, grep
- system: bash, lsp
- info: web_fetch, web_search
- interactive: ask (question)
- tasks: todo, task, plan
- advanced: agent, notebook, worktree, team, tool_search
"""
from agent_tools import filesystem, system, info, interactive, tasks, advanced

__version__ = "0.1.0"

__all__ = [
    "filesystem",
    "system",
    "info",
    "interactive",
    "tasks",
    "advanced",
]