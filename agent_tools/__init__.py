"""Agent Tools - AI 代理工具系统

参考: https://github.com/anomalyco/opencode/tree/main/packages/opencode/src/tool
"""
from __future__ import annotations

import subprocess
import re
import json
import html
import glob as globlib
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field

import requests
from pydantic import BaseModel, Field

__version__ = "0.1.0"


# ============ 参数定义 ============

class EmptyArgs(BaseModel):
  """空参数"""
  pass


class BashArgs(BaseModel):
  """Bash 命令参数"""
  command: str = Field(..., description="Shell command to execute")
  timeout: int = Field(60, ge=1, le=600, description="Timeout in seconds")
  workdir: str = Field("", description="Working directory")


class ReadArgs(BaseModel):
  """读取文件参数"""
  file_path: str = Field(..., description="Path to file")
  offset: int = Field(0, ge=0, description="Line offset")
  limit: int = Field(200, ge=1, le=5000, description="Max lines")


class WriteArgs(BaseModel):
  """写入文件参数"""
  file_path: str = Field(..., description="Path to file")
  content: str = Field(..., description="File content")


class EditArgs(BaseModel):
  """编辑文件参数"""
  file_path: str = Field(..., description="Path to file")
  old_string: str = Field(..., description="String to replace")
  new_string: str = Field(..., description="Replacement string")
  replace_all: bool = Field(False, description="Replace all occurrences")


class MultiEditItem(BaseModel):
  """多重编辑项"""
  old_string: str = Field(..., description="String to replace")
  new_string: str = Field(..., description="Replacement string")


class MultiEditArgs(BaseModel):
  """多重编辑参数"""
  file_path: str = Field(..., description="Path to file")
  edits: list[MultiEditItem] = Field(..., description="Ordered edits")


class GlobArgs(BaseModel):
  """Glob 搜索参数"""
  pattern: str = Field(..., description="Glob pattern")
  path: str = Field(".", description="Base path")
  limit: int = Field(200, ge=1, le=5000, description="Max results")


class GrepArgs(BaseModel):
  """Grep 搜索参数"""
  pattern: str = Field(..., description="Regex pattern")
  path: str = Field(".", description="Base path")
  limit: int = Field(200, ge=1, le=5000, description="Max matches")


class ListArgs(BaseModel):
  """目录列表参数"""
  path: str = Field(".", description="Directory path")
  recursive: bool = Field(False, description="Recursive listing")
  include_hidden: bool = Field(False, description="Include dotfiles")


class WebFetchArgs(BaseModel):
  """网页抓取参数"""
  url: str = Field(..., description="URL to fetch")
  max_chars: int = Field(12000, ge=200, le=200000, description="Max chars to return")


class WebSearchArgs(BaseModel):
  """网页搜索参数"""
  query: str = Field(..., description="Search query")
  limit: int = Field(5, ge=1, le=20, description="Max results")


class TodoItem(BaseModel):
  """Todo 项"""
  content: str = Field(..., description="Todo content")
  status: str = Field("pending", description="pending|in_progress|completed|cancelled")


class TodoWriteArgs(BaseModel):
  """Todo 写入参数"""
  action: str = Field("add", description="add|replace|clear")
  items: list[TodoItem] = Field(default_factory=list, description="Todo items")


class TaskArgs(BaseModel):
  """任务参数"""
  description: str = Field(..., description="3-5 words description")
  prompt: str = Field(..., description="Subtask prompt")
  subagent_type: str = Field("default", description="Subagent type")
  task_id: str = Field("", description="Optional task id")


class LspArgs(BaseModel):
  """LSP 参数"""
  action: str = Field("definition", description="definition|references|hover|document_symbols|completion")
  file_path: str = Field(..., description="File path")
  line: int = Field(1, ge=1, description="Line number (1-based)")
  character: int = Field(1, ge=1, description="Character offset (1-based)")


class PlanEnterArgs(BaseModel):
  """进入规划模式参数"""
  objective: str = Field("", description="Plan objective")
  file_path: str = Field(".plan.md", description="Plan file path")


class QuestionArgs(BaseModel):
  """提问参数"""
  question: str = Field(..., description="Question to ask the user")
  options: list[str] = Field(default_factory=list, description="Optional choices")


# ============ 状态管理 ============

@dataclass
class ToolState:
  """工具状态"""
  root: Path = field(default_factory=Path.cwd)
  workdir: Path = field(default_factory=Path.cwd)
  plan_mode: bool = False
  plan_file: Path = field(default_factory=Path)
  todos: list[dict[str, str]] = field(default_factory=list)

  def resolve(self, path: str) -> Path:
    """解析路径"""
    p = Path(path).expanduser()
    if p.is_absolute():
      return p.resolve()
    return (self.workdir / p).resolve()

  def can_edit(self, path: Path) -> bool:
    """检查是否可编辑"""
    if not self.plan_mode:
      return True
    return path.resolve() == self.plan_file.resolve()


# ============ 工具实现 ============

# 默认状态
_state = ToolState()


def set_state(state: ToolState) -> None:
  """设置全局状态"""
  global _state
  _state = state


def get_state() -> ToolState:
  """获取全局状态"""
  return _state


def _edit_guard(path: Path) -> str | None:
  """编辑保护"""
  if _state.can_edit(path):
    return None
  return f"Denied by plan mode. Only plan file is editable: {_state.plan_file}"


def bash(command: str, timeout: int = 60, workdir: str = "") -> str:
  """执行 Bash 命令

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/bash.ts
  """
  if _state.plan_mode:
    return "Denied by plan mode. Bash is disabled while plan mode is active."

  cwd = Path(workdir) if workdir else _state.workdir
  proc = subprocess.run(
    command,
    cwd=cwd,
    shell=True,
    text=True,
    capture_output=True,
    timeout=timeout,
  )
  out = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
  return f"exit_code={proc.returncode}\n{out.strip()}"


def read(file_path: str, offset: int = 0, limit: int = 200) -> str:
  """读取文件

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/read.ts
  """
  path = _state.resolve(file_path)
  if not path.exists():
    return f"File not found: {path}"
  text = path.read_text(encoding="utf-8")
  lines = text.splitlines()
  chunk = lines[offset : offset + limit]
  header = f"file={path}\nlines={offset + 1}-{offset + len(chunk)}"
  return header + "\n" + "\n".join(chunk)


def write(file_path: str, content: str) -> str:
  """写入文件

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/write.ts
  """
  path = _state.resolve(file_path)
  denied = _edit_guard(path)
  if denied:
    return denied
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(content, encoding="utf-8")
  return f"Wrote {path} ({len(content)} chars)."


def edit(file_path: str, old_string: str, new_string: str, replace_all: bool = False) -> str:
  """编辑文件

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/edit.ts
  """
  path = _state.resolve(file_path)
  denied = _edit_guard(path)
  if denied:
    return denied

  if not path.exists():
    return f"File not found: {path}"

  if old_string == new_string:
    return "No changes: old_string and new_string are identical."

  text = path.read_text(encoding="utf-8")
  if old_string not in text:
    return "Target string not found."

  if replace_all:
    count = text.count(old_string)
    text = text.replace(old_string, new_string)
  else:
    count = 1
    text = text.replace(old_string, new_string, 1)

  path.write_text(text, encoding="utf-8")
  return f"Applied {count} edit(s) successfully."


def multiedit(file_path: str, edits: list[MultiEditItem]) -> str:
  """多重编辑

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/multiedit.ts
  """
  path = _state.resolve(file_path)
  denied = _edit_guard(path)
  if denied:
    return denied

  text = path.read_text(encoding="utf-8")
  changed = 0
  for item in edits:
    if item.old_string in text:
      text = text.replace(item.old_string, item.new_string, 1)
      changed += 1
  path.write_text(text, encoding="utf-8")
  return f"Applied {changed}/{len(edits)} edits."


def glob_tool(pattern: str, path: str = ".", limit: int = 200) -> str:
  """Glob 搜索

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/glob.ts
  """
  base = _state.resolve(path)
  query = str((base / pattern).as_posix())
  hits = globlib.glob(query, recursive=True)
  return "\n".join(hits[:limit])


def grep(pattern: str, path: str = ".", limit: int = 200) -> str:
  """Grep 搜索

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/grep.ts
  """
  base = _state.resolve(path)
  rx = re.compile(pattern)
  out: list[str] = []
  for file in base.rglob("*"):
    if not file.is_file():
      continue
    if file.stat().st_size > 1_000_000:
      continue
    try:
      text = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
      continue
    for idx, line in enumerate(text.splitlines(), start=1):
      if rx.search(line):
        out.append(f"{file}:{idx}:{line}")
        if len(out) >= limit:
          return "\n".join(out)
  return "\n".join(out)


def list_dir(path: str = ".", recursive: bool = False, include_hidden: bool = False) -> str:
  """目录列表

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/ls.ts
  """
  base = _state.resolve(path)
  files = [p for p in base.rglob("*")] if recursive else [p for p in base.iterdir()]
  rows = []
  for p in files:
    rel = p.relative_to(_state.workdir)
    if not include_hidden and any(part.startswith(".") for part in Path(rel).parts):
      continue
    kind = "dir" if p.is_dir() else "file"
    rows.append(f"{kind}\t{rel}")
  return "\n".join(rows[:2000])


def webfetch(url: str, max_chars: int = 12000) -> str:
  """网页抓取

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/webfetch.ts
  """
  response = requests.get(url, timeout=20)
  response.raise_for_status()
  return response.text[:max_chars]


def websearch(query: str, limit: int = 5) -> str:
  """网页搜索

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/websearch.ts
  """
  response = requests.get("https://duckduckgo.com/html/", params={"q": query}, timeout=20)
  response.raise_for_status()
  hits = re.findall(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', response.text)
  rows = []
  for idx, (url, title) in enumerate(hits[:limit], start=1):
    clean = re.sub("<[^>]+>", "", html.unescape(title)).strip()
    rows.append(f"{idx}. {clean}\n{url}")
  if rows:
    return "\n\n".join(rows)
  return "No search result parsed from DuckDuckGo HTML endpoint."


def todowrite(action: str = "add", items: list[TodoItem] | list[dict] | None = None) -> str:
  """写入 Todo

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todo.ts
  """
  if action == "clear":
    _state.todos = []
    return "Todo list cleared."
  items = items or []
  # 支持 dict 和 TodoItem
  normalized = []
  for item in items:
    if isinstance(item, dict):
      normalized.append({"content": item.get("content", ""), "status": item.get("status", "pending")})
    else:
      normalized.append({"content": item.content, "status": item.status})

  if action == "replace":
    _state.todos = normalized
    return json.dumps(_state.todos, ensure_ascii=False, indent=2)
  _state.todos.extend(normalized)
  return json.dumps(_state.todos, ensure_ascii=False, indent=2)


def todoread() -> str:
  """读取 Todo

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todo.ts
  """
  return json.dumps(_state.todos, ensure_ascii=False, indent=2)


def task(description: str, prompt: str, subagent_type: str = "default", task_id: str = "") -> str:
  """创建任务

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/task.ts
  """
  # 占位实现 - 实际使用需要 LLM 集成
  return f"<task_result description='{description}'>\nTask '{subagent_type}' created with prompt: {prompt[:100]}...\n</task_result>"


def lsp(action: str = "definition", file_path: str = "", line: int = 1, character: int = 1) -> str:
  """LSP 操作

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/lsp.ts
  """
  path = _state.resolve(file_path)
  if not path.exists():
    return f"File not found: {path}"

  try:
    import jedi
  except ImportError:
    return "jedi not installed. Run: pip install jedi"

  with open(path, 'r', encoding='utf-8') as f:
    source = f.read()

  script = jedi.Script(code=source, path=str(path))

  result = []
  # Jedi 使用 1-based 行号
  if action == "definition":
    defs = script.goto(line=line, column=character - 1)
    for d in defs:
      if d.module_path:
        result.append(f"{d.module_path}:{d.line}:{d.column} - {d.name}")
  elif action == "references":
    refs = script.get_references(line=line, column=character - 1)
    for r in refs:
      if r.module_path:
        result.append(f"{r.module_path}:{r.line}:{r.column} - {r.name}")
  elif action == "hover":
    help_items = script.help(line=line, column=character - 1)
    for h in help_items:
      if h.docstring():
        result.append(h.docstring()[:500])
  elif action == "document_symbols":
    names = script.get_names()
    for name in names:
      result.append(f"{name.line}:{name.column} - {name.name} ({name.type})")
  elif action == "completion":
    completions = script.complete(line=line, column=character - 1)
    for c in completions[:50]:
      result.append(f"{c.name} ({c.type})")
  else:
    return f"Unknown action: {action}"

  return "\n".join(result) if result else f"No results for {action}"


def plan_enter(objective: str = "", file_path: str = ".plan.md") -> str:
  """进入规划模式

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/plan.ts
  """
  _state.plan_mode = True
  _state.plan_file = _state.resolve(file_path)
  _state.plan_file.parent.mkdir(parents=True, exist_ok=True)
  if not _state.plan_file.exists():
    seed = "# Plan\n\n" + (objective.strip() or "No objective provided.") + "\n"
    _state.plan_file.write_text(seed, encoding="utf-8")
  return f"Plan mode enabled. Only editable file: {_state.plan_file}"


def plan_exit() -> str:
  """退出规划模式

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/plan.ts
  """
  _state.plan_mode = False
  return "Plan mode disabled."


def question(question_text: str, options: list[str] | None = None) -> str:
  """向用户提问

  参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/question.ts
  """
  opts = f" Options: {', '.join(options)}" if options else ""
  return f"QUESTION_FOR_USER: {question_text}{opts}"


__all__ = [
  # 状态
  "ToolState",
  "set_state",
  "get_state",
  # 参数
  "EmptyArgs",
  "BashArgs",
  "ReadArgs",
  "WriteArgs",
  "EditArgs",
  "MultiEditArgs",
  "MultiEditItem",
  "GlobArgs",
  "GrepArgs",
  "ListArgs",
  "WebFetchArgs",
  "WebSearchArgs",
  "TodoItem",
  "TodoWriteArgs",
  "TaskArgs",
  "LspArgs",
  "PlanEnterArgs",
  "QuestionArgs",
  # 工具函数
  "bash",
  "read",
  "write",
  "edit",
  "multiedit",
  "glob_tool",
  "grep",
  "list_dir",
  "webfetch",
  "websearch",
  "todowrite",
  "todoread",
  "task",
  "lsp",
  "plan_enter",
  "plan_exit",
  "question",
]