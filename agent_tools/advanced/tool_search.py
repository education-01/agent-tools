"""工具搜索工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any


class ToolSearchInput(BaseModel):
    """工具搜索输入"""
    query: str = Field(description="搜索关键词")


class ToolInfo(BaseModel):
    """工具信息"""
    name: str
    description: str
    module: str


class ToolSearchOutput(BaseModel):
    """工具搜索输出"""
    success: bool = Field(description="是否成功")
    tools: List[ToolInfo] = Field(description="工具列表")


# 已注册的工具
_REGISTERED_TOOLS = [
    ToolInfo(name="read_file", description="读取文件内容", module="filesystem"),
    ToolInfo(name="write_file", description="写入文件内容", module="filesystem"),
    ToolInfo(name="edit_file", description="编辑文件内容", module="filesystem"),
    ToolInfo(name="glob_files", description="搜索文件 (glob 模式)", module="filesystem"),
    ToolInfo(name="grep_files", description="搜索文件内容", module="filesystem"),
    ToolInfo(name="run_bash", description="执行 Bash 命令", module="system"),
    ToolInfo(name="lsp_request", description="LSP 代码理解", module="system"),
    ToolInfo(name="fetch_web", description="抓取网页内容", module="info"),
    ToolInfo(name="search_web", description="搜索网页", module="info"),
    ToolInfo(name="ask_user", description="向用户提问", module="interactive"),
    ToolInfo(name="write_todo", description="写入 Todo 列表", module="tasks"),
    ToolInfo(name="read_todo", description="读取 Todo 列表", module="tasks"),
    ToolInfo(name="create_task", description="创建任务", module="tasks"),
    ToolInfo(name="list_tasks", description="列出任务", module="tasks"),
    ToolInfo(name="enter_plan_mode", description="进入规划模式", module="tasks"),
    ToolInfo(name="exit_plan_mode", description="退出规划模式", module="tasks"),
    ToolInfo(name="spawn_agent", description="生成子代理", module="advanced"),
    ToolInfo(name="edit_notebook", description="编辑 Notebook", module="advanced"),
    ToolInfo(name="create_worktree", description="创建 Worktree", module="advanced"),
    ToolInfo(name="collaborate", description="团队协作", module="advanced"),
    ToolInfo(name="search_tools", description="搜索工具", module="advanced"),
]


def search_tools(query: str) -> ToolSearchOutput:
    """
    搜索可用工具
    
    参数:
        query: 搜索关键词
    """
    query_lower = query.lower()
    matched = [
        tool for tool in _REGISTERED_TOOLS
        if query_lower in tool.name.lower() 
        or query_lower in tool.description.lower()
        or query_lower in tool.module.lower()
    ]
    
    return ToolSearchOutput(
        success=True,
        tools=matched
    )