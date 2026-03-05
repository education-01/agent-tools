# -*- coding: utf-8 -*-
"""
Agent Tools - 完整的 Agent 工具系统

参考:
- https://github.com/anthropics/claude-code
- https://github.com/mariozechner/pi-coding-agent
- https://github.com/openai/openai-agents-python

功能模块:
- filesystem: 文件系统操作 (Read, Write, Edit, Glob, Grep)
- system: 系统执行 (Bash)
- info: 信息获取 (WebFetch, WebSearch)
- interactive: 用户交互 (AskUserQuestion)
- tasks: 任务管理 (Todo, Task, Plan)
- advanced: 高级能力 (Agent, Notebook, Worktree, Team, ToolSearch)
"""

from agent_tools import filesystem, system, info, interactive, tasks, advanced

__version__ = "0.1.0"
__all__ = ["filesystem", "system", "info", "interactive", "tasks", "advanced"]