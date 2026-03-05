"""批量调用工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/batch.ts
"""
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class BatchCall(BaseModel):
    """批量调用项"""
    tool: str = Field(description="Tool name")
    input: Dict[str, Any] = Field(default_factory=dict, description="Tool input")


class BatchInput(BaseModel):
    """批量调用输入"""
    calls: List[BatchCall] = Field(description="List of tool calls to execute")


class BatchResult(BaseModel):
    """单个调用结果"""
    index: int = Field(description="Call index (1-based)")
    tool: str = Field(description="Tool name")
    status: str = Field(description="ok | error | unknown")
    output: Optional[str] = Field(default=None, description="Tool output")
    error: Optional[str] = Field(default=None, description="Error message")


class BatchOutput(BaseModel):
    """批量调用输出"""
    results: List[BatchResult] = Field(description="List of results")
    total: int = Field(description="Total calls")
    success: int = Field(description="Successful calls")
    failed: int = Field(description="Failed calls")


# 工具执行映射 - 延迟导入避免循环依赖
_EXEC_MAP: Dict[str, Any] = {}


def _init_exec_map() -> None:
    """初始化工具执行映射"""
    global _EXEC_MAP
    if _EXEC_MAP:
        return
    
    from ..filesystem import read_file, write_file, edit_file
    from ..filesystem.glob import glob_files
    from ..filesystem.grep import grep_files
    from ..system.bash import run_bash
    from ..system.lsp import lsp_request
    from ..info.web_fetch import fetch_web
    from ..info.web_search import search_web
    from ..interactive.ask import ask_user
    from ..tasks.todo import write_todo, read_todo
    from ..tasks.task import create_task, list_tasks
    from ..tasks.plan import enter_plan_mode, exit_plan_mode
    
    _EXEC_MAP = {
        "read": read_file,
        "write": write_file,
        "edit": edit_file,
        "glob": glob_files,
        "grep": grep_files,
        "bash": run_bash,
        "lsp": lsp_request,
        "webfetch": fetch_web,
        "websearch": search_web,
        "question": ask_user,
        "todowrite": write_todo,
        "todoread": read_todo,
        "task": create_task,
        "plan_enter": enter_plan_mode,
        "plan_exit": exit_plan_mode,
    }


def batch_execute(calls: List[Dict[str, Any]]) -> BatchOutput:
    """
    批量执行工具调用
    
    参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/batch.ts
    
    参数:
        calls: 工具调用列表，每个包含 tool 和 input
        
    返回:
        BatchOutput: 包含所有调用结果
    """
    _init_exec_map()
    
    results: List[BatchResult] = []
    success = 0
    failed = 0
    
    for idx, call in enumerate(calls, start=1):
        name = call.get("tool", "")
        payload = call.get("input", {})
        
        fn = _EXEC_MAP.get(name)
        
        if not fn:
            results.append(BatchResult(
                index=idx,
                tool=name,
                status="unknown",
                error=f"Unknown tool: {name}"
            ))
            failed += 1
            continue
            
        if name == "batch":
            results.append(BatchResult(
                index=idx,
                tool=name,
                status="error",
                error="Nested batch is not allowed"
            ))
            failed += 1
            continue
        
        try:
            out = fn(**payload)
            # 处理 Pydantic 模型输出
            if hasattr(out, 'model_dump'):
                output_str = str(out.model_dump())
            else:
                output_str = str(out)
            
            results.append(BatchResult(
                index=idx,
                tool=name,
                status="ok",
                output=output_str
            ))
            success += 1
        except Exception as error:
            results.append(BatchResult(
                index=idx,
                tool=name,
                status="error",
                error=str(error)
            ))
            failed += 1
    
    return BatchOutput(
        results=results,
        total=len(calls),
        success=success,
        failed=failed
    )
