"""Todo 任务列表工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todo.ts
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from pathlib import Path
import json


# 参考 OpenCode 的 Todo.Info shape
class TodoItem(BaseModel):
    """Todo 项目 - 参考 OpenCode Todo.Info"""
    content: str = Field(description="任务内容")
    status: str = Field(default="pending", description="状态: pending, in_progress, completed")
    active: bool = Field(default=True, description="是否激活")


class TodoWriteInput(BaseModel):
    """Todo 写入输入 - 参考 OpenCode todowrite"""
    todos: List[TodoItem] = Field(description="The updated todo list")


class TodoReadInput(BaseModel):
    """Todo 读取输入"""
    pass


class TodoOutput(BaseModel):
    """Todo 输出"""
    success: bool = Field(description="是否成功")
    todos: List[TodoItem] = Field(description="任务列表")


_TODO_FILE = Path(".agent-todos.json")
_todos: List[TodoItem] = []


def write_todo(todos: List[TodoItem]) -> TodoOutput:
    """
    写入 Todo 列表
    
    参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todo.ts
    
    参数:
        todos: 任务列表
    """
    global _todos
    _todos = todos
    
    try:
        data = [t.model_dump() for t in todos]
        with open(_TODO_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return TodoOutput(success=True, todos=todos)
    except Exception:
        return TodoOutput(success=True, todos=todos)


def read_todo() -> TodoOutput:
    """
    读取 Todo 列表
    
    参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todo.ts
    """
    global _todos
    
    try:
        if _TODO_FILE.exists():
            with open(_TODO_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            _todos = [TodoItem(**item) for item in data]
    except Exception:
        pass
    
    return TodoOutput(success=True, todos=_todos)