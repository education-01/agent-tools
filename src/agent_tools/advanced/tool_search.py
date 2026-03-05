"""高级 Agent 能力 - ToolSearch 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/toolSearch.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/toolSearch.ts
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import importlib
import pkgutil


class ToolSearchInput(BaseModel):
    query: str = Field(description="搜索关键词")
    category: Optional[str] = Field(default=None, description="工具类别")


class ToolInfo(BaseModel):
    name: str
    module: str
    description: str
    category: str


class ToolSearchOutput(BaseModel):
    success: bool
    tools: Optional[List[ToolInfo]] = None
    error: Optional[str] = None


# 工具注册表
TOOL_REGISTRY: List[ToolInfo] = [
    # 文件系统
    ToolInfo(name="read_file", module="agent_tools.filesystem.read", description="读取文件内容", category="filesystem"),
    ToolInfo(name="write_file", module="agent_tools.filesystem.write", description="写入文件内容", category="filesystem"),
    ToolInfo(name="edit_file", module="agent_tools.filesystem.edit", description="编辑文件内容", category="filesystem"),
    ToolInfo(name="glob_files", module="agent_tools.filesystem.glob", description="匹配文件路径", category="filesystem"),
    ToolInfo(name="grep_files", module="agent_tools.filesystem.grep", description="搜索文件内容", category="filesystem"),
    # 系统执行
    ToolInfo(name="run_bash", module="agent_tools.system.bash", description="执行系统命令", category="system"),
    # 信息获取
    ToolInfo(name="fetch_web", module="agent_tools.info.web_fetch", description="获取网页内容", category="info"),
    ToolInfo(name="search_web", module="agent_tools.info.web_search", description="搜索网页", category="info"),
    # 用户交互
    ToolInfo(name="ask_user", module="agent_tools.interactive.ask", description="向用户提问", category="interactive"),
    # 任务管理
    ToolInfo(name="write_todo", module="agent_tools.tasks.todo", description="写入待办事项", category="tasks"),
    ToolInfo(name="read_todos", module="agent_tools.tasks.todo", description="读取待办事项", category="tasks"),
    ToolInfo(name="create_task", module="agent_tools.tasks.task", description="创建任务", category="tasks"),
    ToolInfo(name="list_tasks", module="agent_tools.tasks.task", description="列出任务", category="tasks"),
    ToolInfo(name="update_task", module="agent_tools.tasks.task", description="更新任务", category="tasks"),
    ToolInfo(name="enter_plan_mode", module="agent_tools.tasks.plan", description="进入规划模式", category="tasks"),
    ToolInfo(name="exit_plan_mode", module="agent_tools.tasks.plan", description="退出规划模式", category="tasks"),
    # 高级能力
    ToolInfo(name="spawn_agent", module="agent_tools.advanced.agent", description="生成子代理", category="advanced"),
    ToolInfo(name="edit_notebook", module="agent_tools.advanced.notebook", description="编辑Notebook", category="advanced"),
    ToolInfo(name="worktree_action", module="agent_tools.advanced.worktree", description="管理Git工作树", category="advanced"),
    ToolInfo(name="team_collab", module="agent_tools.advanced.team", description="团队协作", category="advanced"),
]


def search_tools(query: str, category: str = None) -> ToolSearchOutput:
    """搜索可用工具"""
    try:
        results = []
        query_lower = query.lower()
        
        for tool in TOOL_REGISTRY:
            if category and tool.category != category:
                continue
            
            if query_lower in tool.name.lower() or query_lower in tool.description.lower():
                results.append(tool)
        
        return ToolSearchOutput(success=True, tools=results)
    except Exception as e:
        return ToolSearchOutput(success=False, error=str(e))


def list_all_tools() -> ToolSearchOutput:
    """列出所有工具"""
    return ToolSearchOutput(success=True, tools=TOOL_REGISTRY)


if __name__ == "__main__":
    result = search_tools("read")
    print(f"Found {len(result.tools)} tools:")
    for t in result.tools:
        print(f"  - {t.name}: {t.description}")