"""任务管理工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/task.ts
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskInput(BaseModel):
    """任务输入"""
    action: str = Field(description="操作: create, list, update, stop, output")
    task_id: Optional[str] = Field(default=None, description="任务 ID")
    prompt: Optional[str] = Field(default=None, description="任务提示")
    status: Optional[TaskStatus] = Field(default=None, description="任务状态")


class Task(BaseModel):
    """任务"""
    id: str = Field(description="任务 ID")
    prompt: str = Field(description="任务提示")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    output: Optional[str] = Field(default=None)


class TaskOutput(BaseModel):
    """任务输出"""
    success: bool = Field(description="是否成功")
    tasks: Optional[List[Task]] = Field(default=None, description="任务列表")
    task: Optional[Task] = Field(default=None, description="单个任务")
    error: Optional[str] = Field(default=None, description="错误信息")


# 内存中的任务存储
_tasks: Dict[str, Task] = {}


def create_task(prompt: str) -> TaskOutput:
    """
    创建新任务
    
    参数:
        prompt: 任务提示
    """
    task_id = str(uuid.uuid4())[:8]
    task = Task(id=task_id, prompt=prompt)
    _tasks[task_id] = task
    return TaskOutput(success=True, task=task)


def list_tasks() -> TaskOutput:
    """
    列出所有任务
    """
    return TaskOutput(
        success=True,
        tasks=list(_tasks.values())
    )


def update_task(task_id: str, status: TaskStatus, output: str = None) -> TaskOutput:
    """
    更新任务状态
    
    参数:
        task_id: 任务 ID
        status: 新状态
        output: 任务输出
    """
    if task_id not in _tasks:
        return TaskOutput(success=False, error=f"Task {task_id} not found")
    
    task = _tasks[task_id]
    task.status = status
    if output:
        task.output = output
    
    return TaskOutput(success=True, task=task)