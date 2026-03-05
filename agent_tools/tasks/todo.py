"""Todo 任务列表工具

参考: 
- https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todo.ts
- https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todowrite.txt
- https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/todoread.txt
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from pathlib import Path
import json


class TodoItem(BaseModel):
    """Todo 项目"""
    content: str = Field(description="任务内容")
    active: bool = Field(default=True, description="是否激活")
    status: str = Field(default="pending", description="状态: pending, in_progress, completed")


class TodoInput(BaseModel):
    """Todo 输入"""
    todos: List[TodoItem] = Field(description="任务列表")


class TodoOutput(BaseModel):
    """Todo 输出"""
    success: bool = Field(description="是否成功")
    todos: List[TodoItem] = Field(description="任务列表")


TODO_FILE = Path(".agent-todos.json")


def write_todo(todos: List[TodoItem]) -> TodoOutput:
    """
    写入 Todo 列表
    
    参数:
        todos: 任务列表
    """
    try:
        data = [t.model_dump() for t in todos]
        with open(TODO_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return TodoOutput(success=True, todos=todos)
    except Exception as e:
        return TodoOutput(success=False, todos=[])


def read_todo() -> TodoOutput:
    """
    读取 Todo 列表
    """
    try:
        if not TODO_FILE.exists():
            return TodoOutput(success=True, todos=[])
        
        with open(TODO_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        todos = [TodoItem(**item) for item in data]
        return TodoOutput(success=True, todos=todos)
    except Exception:
        return TodoOutput(success=False, todos=[])