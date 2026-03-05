# Agent Tools

A comprehensive Agent Tool System for AI agents.参考 [OpenCode](https://github.com/anomalyco/opencode/tree/main/packages/opencode/src/tool) 实现。

## 安装

```bash
pip install -e .
# 可选：LSP 支持
pip install jedi
```

## 使用

```python
from agent_tools import (
  bash, read, write, edit, glob_tool, grep, list_dir,
  webfetch, websearch, todowrite, todoread, task, lsp,
  plan_enter, plan_exit, question,
  ToolState, set_state,
)

# 设置工作目录
state = ToolState(workdir=Path("/path/to/project"))
set_state(state)

# 读取文件
content = read("src/main.py", offset=0, limit=100)

# 执行命令
result = bash("npm test", timeout=60)

# 编辑文件
edit("src/main.py", "old_code", "new_code")

# Glob 搜索
files = glob_tool("**/*.py")

# Grep 搜索
matches = grep("import", path="src")

# Todo 管理
todowrite("add", [{"content": "Fix bug", "status": "pending"}])
todos = todoread()

# LSP (需要安装 jedi)
definitions = lsp("definition", "src/main.py", line=10, character=5)

# 规划模式
plan_enter("Implement feature X")
# ... 只能编辑 .plan.md 文件
plan_exit()
```

## 工具列表

| 工具 | 描述 | 参考 |
|------|------|------|
| `bash` | 执行 Shell 命令 | [bash.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/bash.ts) |
| `read` | 读取文件 | [read.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/read.ts) |
| `write` | 写入文件 | [write.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/write.ts) |
| `edit` | 编辑文件 | [edit.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/edit.ts) |
| `multiedit` | 多重编辑 | [multiedit.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/multiedit.ts) |
| `glob_tool` | Glob 搜索 | [glob.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/glob.ts) |
| `grep` | Grep 搜索 | [grep.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/grep.ts) |
| `list_dir` | 目录列表 | [ls.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/ls.ts) |
| `webfetch` | 网页抓取 | [webfetch.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/webfetch.ts) |
| `websearch` | 网页搜索 | [websearch.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/websearch.ts) |
| `todowrite` | 写入 Todo | [todo.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todo.ts) |
| `todoread` | 读取 Todo | [todo.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todo.ts) |
| `task` | 创建任务 | [task.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/task.ts) |
| `lsp` | LSP 操作 | [lsp.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/lsp.ts) |
| `plan_enter` | 进入规划模式 | [plan.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/plan.ts) |
| `plan_exit` | 退出规划模式 | [plan.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/plan.ts) |
| `question` | 向用户提问 | [question.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/question.ts) |

## License

MIT