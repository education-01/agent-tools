"""Git Worktree 工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool
"""
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path
import subprocess


class WorktreeInput(BaseModel):
    """Worktree 输入"""
    action: str = Field(description="操作: create, list, remove")
    branch: Optional[str] = Field(default=None, description="分支名")
    path: Optional[str] = Field(default=None, description="路径")


class WorktreeInfo(BaseModel):
    """Worktree 信息"""
    path: str
    branch: str
    commit: str


class WorktreeOutput(BaseModel):
    """Worktree 输出"""
    success: bool = Field(description="是否成功")
    worktrees: Optional[list] = Field(default=None, description="worktree 列表")
    error: Optional[str] = Field(default=None, description="错误信息")


def create_worktree(branch: str, path: str = None) -> WorktreeOutput:
    """
    创建 Git Worktree
    
    参数:
        branch: 分支名
        path: 目标路径 (可选)
    """
    try:
        cmd = ["git", "worktree", "add"]
        if path:
            cmd.append(path)
        cmd.append(branch)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return WorktreeOutput(success=True)
        else:
            return WorktreeOutput(success=False, error=result.stderr)
    except Exception as e:
        return WorktreeOutput(success=False, error=str(e))


def list_worktrees() -> WorktreeOutput:
    """列出所有 Git Worktrees"""
    try:
        result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return WorktreeOutput(success=True, worktrees=[result.stdout])
        else:
            return WorktreeOutput(success=False, error=result.stderr)
    except Exception as e:
        return WorktreeOutput(success=False, error=str(e))