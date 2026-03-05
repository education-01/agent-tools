# Agent Tools

A comprehensive Agent Tool System for AI agents.

## 参考

所有工具实现参考 [OpenCode](https://github.com/anomalyco/opencode/tree/main/packages/opencode/src/tool)：

| 模块 | 工具 | 参考 |
|------|------|------|
| filesystem | read, write, edit, glob, grep | [read.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/read.ts), [write.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/write.ts), [edit.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/edit.ts), [glob.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/glob.ts), [grep.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/grep.ts) |
| system | bash, lsp | [bash.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/bash.ts), [lsp.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/lsp.ts) |
| info | web_fetch, web_search | [webfetch.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/webfetch.ts), [websearch.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/websearch.ts) |
| interactive | ask | [question.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/question.ts) |
| tasks | todo, task, plan | [todo.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todo.ts), [task.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/task.ts), [plan.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/plan.ts) |

## 安装

```bash
pip install -e .
```

## 使用

```python
from agent_tools.filesystem import read_file, write_file, edit_file
from agent_tools.system import run_bash, lsp_request
from agent_tools.info import fetch_web, search_web
from agent_tools.interactive import ask_user
from agent_tools.tasks import write_todo, read_todo, create_task
from agent_tools.advanced import search_tools

# 读取文件
result = read_file("/path/to/file.py", offset=1, limit=100)
print(result.content)

# 执行命令
result = run_bash("ls -la", description="List files in current directory")
print(result.stdout)

# LSP 操作
result = lsp_request("goToDefinition", "/path/to/file.py", line=10, character=5)
print(result.result)
```

## 依赖

- Python >= 3.12
- pydantic >= 2.0
- jedi >= 0.19 (for LSP)

## License

MIT