"""任务管理 - Task 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/task.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/task.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List, Dict, Any
import json
from datetime import datetime


class Task(BaseModel):
    id: str
    name: str
    description: str
    status: str = "pending"  # pending, running, completed, failed, stopped
    progress: int = 0
    output: Optional[str] = None
    error: Optional[str] = None
    created_at: str
    updated_at: str


class TaskCreateInput(BaseModel):
    name: str = Field(description="任务名称")
    description: str = Field(default="", description="任务描述")


class TaskListInput(BaseModel):
    status: Optional[str] = Field(default=None, description="按状态过滤")


class TaskUpdateInput(BaseModel):
    id: str = Field(description="任务ID")
    status: Optional[str] = Field(default=None)
    progress: Optional[int] = Field(default=None)
    output: Optional[str] = Field(default=None)
    error: Optional[str] = Field(default=None)


class TaskStopInput(BaseModel):
    id: str = Field(description="任务ID")


class TaskOutputInput(BaseModel):
    id: str = Field(description="任务ID")


class TaskOutput(BaseModel):
    success: bool
    task: Optional[Task] = None
    tasks: Optional[List[Task]] = None
    error: Optional[str] = None


TASK_FILE = Path.home() / ".agent_tools" / "tasks.json"


def _load_tasks() -> Dict[str, Task]:
    if not TASK_FILE.exists():
        return {}
    try:
        data = json.loads(TASK_FILE.read_text())
        return {k: Task(**v) for k, v in data.items()}
    except Exception:
        return {}


def _save_tasks(tasks: Dict[str, Task]):
    TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
    TASK_FILE.write_text(json.dumps({k: v.model_dump() for k, v in tasks.items()}, indent=2, ensure_ascii=False))


def create_task(name: str, description: str = "") -> TaskOutput:
    """创建任务"""
    try:
        tasks = _load_tasks()
        task_id = str(len(tasks) + 1)
        task = Task(
            id=task_id,
            name=name,
            description=description,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        tasks[task_id] = task
        _save_tasks(tasks)
        return TaskOutput(success=True, task=task)
    except Exception as e:
        return TaskOutput(success=False, error=str(e))


def list_tasks(status: Optional[str] = None) -> TaskOutput:
    """列出任务"""
    try:
        tasks = _load_tasks()
        result = list(tasks.values())
        if status:
            result = [t for t in result if t.status == status]
        return TaskOutput(success=True, tasks=result)
    except Exception as e:
        return TaskOutput(success=False, error=str(e))


def update_task(id: str, status: Optional[str] = None, progress: Optional[int] = None, 
                output: Optional[str] = None, error: Optional[str] = None) -> TaskOutput:
    """更新任务"""
    try:
        tasks = _load_tasks()
        if id not in tasks:
            return TaskOutput(success=False, error=f"Task {id} not found")
        
        task = tasks[id]
        if status:
            task.status = status
        if progress is not None:
            task.progress = progress
        if output:
            task.output = output
        if error:
            task.error = error
        task.updated_at = datetime.now().isoformat()
        
        _save_tasks(tasks)
        return TaskOutput(success=True, task=task)
    except Exception as e:
        return TaskOutput(success=False, error=str(e))


def stop_task(id: str) -> TaskOutput:
    """停止任务"""
    return update_task(id, status="stopped")


def get_task_output(id: str) -> TaskOutput:
    """获取任务输出"""
    try:
        tasks = _load_tasks()
        if id not in tasks:
            return TaskOutput(success=False, error=f"Task {id} not found")
        return TaskOutput(success=True, task=tasks[id])
    except Exception as e:
        return TaskOutput(success=False, error=str(e))


if __name__ == "__main__":
    # 测试
    r1 = create_task("测试任务", "这是一个测试")
    print(f"Created: {r1.success}, ID: {r1.task.id if r1.task else None}")
    
    r2 = list_tasks()
    print(f"List: {r2.success}, Count: {len(r2.tasks) if r2.tasks else 0}")