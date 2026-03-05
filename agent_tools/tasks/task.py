"""任务管理工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/task.ts
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum
import uuid


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# 参考 OpenCode 的参数
class TaskInput(BaseModel):
    """任务输入 - 参考 OpenCode task.ts 参数"""
    description: str = Field(description="A short (3-5 words) description of the task")
    prompt: str = Field(description="The task for the agent to perform")
    subagent_type: str = Field(default="default", description="The type of specialized agent to use")
    task_id: Optional[str] = Field(
        default=None,
        description="Resume a previous task by passing a prior task_id"
    )
    command: Optional[str] = Field(default=None, description="The command that triggered this task")


class Task(BaseModel):
    """任务"""
    id: str = Field(description="Task ID")
    description: str = Field(description="Task description")
    prompt: str = Field(description="Task prompt")
    subagent_type: str = Field(description="Subagent type")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    output: Optional[str] = Field(default=None)


class TaskOutput(BaseModel):
    """任务输出"""
    success: bool = Field(description="是否成功")
    task: Optional[Task] = Field(default=None, description="创建的任务")
    tasks: Optional[List[Task]] = Field(default=None, description="任务列表")
    error: Optional[str] = Field(default=None, description="错误信息")


_tasks: Dict[str, Task] = {}


def create_task(
    description: str,
    prompt: str,
    subagent_type: str = "default",
    task_id: str = None
) -> TaskOutput:
    """
    创建任务
    
    参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/task.ts
    
    参数:
        description: 简短描述（3-5 个词）
        prompt: 任务提示
        subagent_type: 子代理类型
        task_id: 恢复之前的任务 ID
    """
    if task_id and task_id in _tasks:
        task = _tasks[task_id]
        task.status = TaskStatus.RUNNING
        return TaskOutput(success=True, task=task)
    
    new_id = task_id or str(uuid.uuid4())[:8]
    task = Task(
        id=new_id,
        description=description,
        prompt=prompt,
        subagent_type=subagent_type
    )
    _tasks[new_id] = task
    
    return TaskOutput(
        success=True,
        task=task
    )


def list_tasks() -> TaskOutput:
    """列出所有任务"""
    return TaskOutput(
        success=True,
        tasks=list(_tasks.values())
    )