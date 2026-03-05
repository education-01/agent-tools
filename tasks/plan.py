"""规划系统 - Plan 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/plan.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/plan.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List, Dict
import json
from datetime import datetime


class PlanStep(BaseModel):
    id: str
    content: str
    done: bool = False


class Plan(BaseModel):
    id: str
    title: str
    steps: List[PlanStep] = []
    active: bool = False
    created_at: str
    updated_at: str


class EnterPlanInput(BaseModel):
    title: str = Field(description="计划标题")
    steps: List[str] = Field(default=[], description="计划步骤列表")


class ExitPlanInput(BaseModel):
    id: str = Field(description="计划ID")


class PlanOutput(BaseModel):
    success: bool
    plan: Optional[Plan] = None
    plans: Optional[List[Plan]] = None
    error: Optional[str] = None


PLAN_FILE = Path.home() / ".agent_tools" / "plans.json"


def _load_plans() -> Dict[str, Plan]:
    if not PLAN_FILE.exists():
        return {}
    try:
        data = json.loads(PLAN_FILE.read_text())
        return {k: Plan(**v) for k, v in data.items()}
    except Exception:
        return {}


def _save_plans(plans: Dict[str, Plan]):
    PLAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    PLAN_FILE.write_text(json.dumps({k: v.model_dump() for k, v in plans.items()}, indent=2, ensure_ascii=False))


def enter_plan_mode(title: str, steps: List[str] = None) -> PlanOutput:
    """进入规划模式，创建新计划"""
    try:
        plans = _load_plans()
        plan_id = str(len(plans) + 1)
        
        plan_steps = [
            PlanStep(id=str(i+1), content=step) 
            for i, step in enumerate(steps or [])
        ]
        
        plan = Plan(
            id=plan_id,
            title=title,
            steps=plan_steps,
            active=True,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # 将其他计划设为非活动
        for p in plans.values():
            p.active = False
        
        plans[plan_id] = plan
        _save_plans(plans)
        return PlanOutput(success=True, plan=plan)
    except Exception as e:
        return PlanOutput(success=False, error=str(e))


def exit_plan_mode(id: str) -> PlanOutput:
    """退出规划模式"""
    try:
        plans = _load_plans()
        if id not in plans:
            return PlanOutput(success=False, error=f"Plan {id} not found")
        
        plans[id].active = False
        plans[id].updated_at = datetime.now().isoformat()
        _save_plans(plans)
        return PlanOutput(success=True, plan=plans[id])
    except Exception as e:
        return PlanOutput(success=False, error=str(e))


def list_plans() -> PlanOutput:
    """列出所有计划"""
    try:
        plans = _load_plans()
        return PlanOutput(success=True, plans=list(plans.values()))
    except Exception as e:
        return PlanOutput(success=False, error=str(e))


if __name__ == "__main__":
    # 测试
    r1 = enter_plan_mode("实现 Agent Tools", ["Read", "Write", "Edit"])
    print(f"Created plan: {r1.success}")
    if r1.plan:
        print(f"Steps: {[s.content for s in r1.plan.steps]}")