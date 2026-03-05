"""任务管理 - Todo 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/todo.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/todo.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List
import json
from datetime import datetime


class TodoItem(BaseModel):
    id: str
    content: str
    done: bool = False
    created_at: str
    updated_at: str


class TodoWriteInput(BaseModel):
    content: str = Field(description="待办事项内容")
    done: bool = Field(default=False, description="是否已完成")


class TodoReadInput(BaseModel):
    pass


class TodoOutput(BaseModel):
    success: bool
    items: Optional[List[TodoItem]] = None
    error: Optional[str] = None


TODO_FILE = Path.home() / ".agent_tools" / "todos.json"


def _load_todos() -> List[TodoItem]:
    """加载待办事项"""
    if not TODO_FILE.exists():
        return []
    try:
        data = json.loads(TODO_FILE.read_text())
        return [TodoItem(**item) for item in data]
    except Exception:
        return []


def _save_todos(todos: List[TodoItem]):
    """保存待办事项"""
    TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
    TODO_FILE.write_text(json.dumps([t.model_dump() for t in todos], indent=2, ensure_ascii=False))


def write_todo(content: str, done: bool = False) -> TodoOutput:
    """写入待办事项"""
    try:
        todos = _load_todos()
        todo = TodoItem(
            id=str(len(todos) + 1),
            content=content,
            done=done,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        todos.append(todo)
        _save_todos(todos)
        return TodoOutput(success=True, items=todos)
    except Exception as e:
        return TodoOutput(success=False, error=str(e))


def read_todos() -> TodoOutput:
    """读取待办事项"""
    try:
        todos = _load_todos()
        return TodoOutput(success=True, items=todos)
    except Exception as e:
        return TodoOutput(success=False, error=str(e))


if __name__ == "__main__":
    # 测试
    write_todo("测试待办1")
    write_todo("测试待办2")
    result = read_todos()
    print(f"Success: {result.success}")
    print(f"Items: {len(result.items)}")
    for t in result.items:
        print(f"  [{t.id}] {t.content} - {t.done}")