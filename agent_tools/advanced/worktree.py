"""Git Worktree 工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool
"""
from pydantic import BaseModel, Field
from typing import Optional, List
import subprocess


class WorktreeInput(BaseModel):
    """Worktree 输入"""
    action: str = Field(default="list", description="操作: create, list, remove")
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
    worktrees: Optional[List[str]] = Field(default=None, description="worktree 列表")
    error: Optional[str] = Field(default=None, description="错误信息")


def create_worktree(branch: str = None, path: str = None, action: str = "create") -> WorktreeOutput:
    """
    Git Worktree 操作
    
    参数:
        branch: 分支名 (create/remove 时需要)
        path: 目标路径 (可选)
        action: 操作类型 (create/list/remove)
    """
    try:
        # list 操作
        if action == "list" or branch == "list":
            result = subprocess.run(
                ["git", "worktree", "list"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                worktrees = result.stdout.strip().split('\n') if result.stdout.strip() else []
                return WorktreeOutput(success=True, worktrees=worktrees)
            else:
                return WorktreeOutput(success=False, error=result.stderr)
        
        # create 操作
        if action == "create":
            if not branch:
                return WorktreeOutput(success=False, error="Branch name required for create action")
            
            # 检查分支是否存在
            check = subprocess.run(
                ["git", "rev-parse", "--verify", branch],
                capture_output=True,
                text=True
            )
            
            cmd = ["git", "worktree", "add"]
            if path:
                cmd.append(path)
            
            # 如果分支不存在，创建新分支
            if check.returncode != 0:
                cmd.extend(["-b", branch])
            else:
                cmd.append(branch)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return WorktreeOutput(success=True)
            else:
                return WorktreeOutput(success=False, error=result.stderr)
        
        # remove 操作
        if action == "remove":
            if not path:
                return WorktreeOutput(success=False, error="Path required for remove action")
            
            result = subprocess.run(
                ["git", "worktree", "remove", path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return WorktreeOutput(success=True)
            else:
                return WorktreeOutput(success=False, error=result.stderr)
        
        return WorktreeOutput(success=False, error=f"Unknown action: {action}")
        
    except Exception as e:
        return WorktreeOutput(success=False, error=str(e))


def list_worktrees() -> WorktreeOutput:
    """列出所有 Git Worktrees"""
    return create_worktree(action="list")
