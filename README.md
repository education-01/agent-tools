# Agent Tools

A comprehensive Agent Tool System for AI agents.

参考 [OpenCode](https://github.com/anomalyco/opencode/tree/main/packages/opencode/src/tool) 实现。

## 目录结构

```
agent_tools/
├── filesystem/     # 文件系统工具
│   ├── read.py
│   ├── write.py
│   ├── edit.py
│   ├── multiedit.py
│   ├── glob.py
│   └── grep.py
│
├── system/         # 系统执行工具
│   ├── bash.py
│   ├── lsp.py
│   └── batch.py
│
├── info/           # 信息获取工具
│   ├── web_fetch.py
│   └── web_search.py
│
├── interactive/    # 用户交互工具
│   └── ask.py
│
├── tasks/          # 任务管理工具
│   ├── todo.py
│   ├── task.py
│   └── plan.py
│
└── advanced/       # 高级 Agent 能力
    ├── agent.py
    ├── notebook.py
    ├── worktree.py
    ├── team.py
    └── tool_search.py
```

## 工具列表

### 文件系统 (filesystem)

| 工具 | 描述 | 参考 |
|------|------|------|
| `read_file` | 读取文件 | [read.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/read.ts) |
| `write_file` | 写入文件 | [write.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/write.ts) |
| `edit_file` | 编辑文件 | [edit.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/edit.ts) |
| `multi_edit` | 多重编辑 | [multiedit.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/multiedit.ts) |
| `glob_files` | Glob 搜索 | [glob.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/glob.ts) |
| `grep_files` | Grep 搜索 | [grep.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/grep.ts) |

### 系统执行 (system)

| 工具 | 描述 | 参考 |
|------|------|------|
| `run_bash` | 执行 Shell 命令 | [bash.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/bash.ts) |
| `lsp_request` | LSP 操作 | [lsp.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/lsp.ts) |
| `batch_execute` | 批量调用工具 | [batch.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/batch.ts) |

### 信息获取 (info)

| 工具 | 描述 | 参考 |
|------|------|------|
| `fetch_web` | 网页抓取 | [webfetch.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/webfetch.ts) |
| `search_web` | 网页搜索 | [websearch.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/websearch.ts) |

### 用户交互 (interactive)

| 工具 | 描述 | 参考 |
|------|------|------|
| `ask_user` | 向用户提问 | [question.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/question.ts) |

### 任务管理 (tasks)

| 工具 | 描述 | 参考 |
|------|------|------|
| `write_todo` | 写入 Todo | [todo.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todo.ts) |
| `read_todo` | 读取 Todo | [todo.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todo.ts) |
| `create_task` | 创建任务 | [task.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/task.ts) |
| `list_tasks` | 列出任务 | [task.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/task.ts) |
| `enter_plan_mode` | 进入规划模式 | [plan.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/plan.ts) |
| `exit_plan_mode` | 退出规划模式 | [plan.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/plan.ts) |

### 高级 Agent 能力 (advanced)

| 工具 | 描述 | 参考 |
|------|------|------|
| `spawn_agent` | 子代理 | [agent.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/agent.ts) |
| `edit_notebook` | Notebook 编辑 | [notebook.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/notebook.ts) |
| `create_worktree` | Git Worktree | [worktree.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/worktree.ts) |
| `collaborate` | 团队协作 | [team.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/team.ts) |
| `search_tools` | 工具搜索 | - |

## License

MIT
