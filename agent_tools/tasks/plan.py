"""规划模式工具

参考: 
- https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/plan.ts
- https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/plan-enter.txt
- https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/plan-exit.txt
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class PlanMode(str, Enum):
    ENTER = "enter"
    EXIT = "exit"


class PlanInput(BaseModel):
    """规划输入"""
    action: PlanMode = Field(description="操作: enter 或 exit")
    plan: Optional[str] = Field(default=None, description="规划内容")


class PlanOutput(BaseModel):
    """规划输出"""
    success: bool = Field(description="是否成功")
    in_plan_mode: bool = Field(description="是否在规划模式")
    plan: Optional[str] = Field(default=None, description="规划内容")


# 规划模式状态
_plan_mode = False
_current_plan = None


def enter_plan_mode() -> PlanOutput:
    """
    进入规划模式
    
    在规划模式下，代理会先制定完整计划再执行。
    """
    global _plan_mode
    _plan_mode = True
    return PlanOutput(success=True, in_plan_mode=True)


def exit_plan_mode(plan: str = None) -> PlanOutput:
    """
    退出规划模式
    
    参数:
        plan: 规划内容
    """
    global _plan_mode, _current_plan
    _plan_mode = False
    _current_plan = plan
    return PlanOutput(success=True, in_plan_mode=False, plan=plan)