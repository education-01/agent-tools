"""高级 Agent 能力 - Worktree 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/worktree.ts
- https://git-scm.com/docs/git-worktree
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional
import subprocess


class WorktreeInput(BaseModel):
    action: str = Field(description="操作: create, list, remove")
    path: Optional[str] = Field(default=None, description="工作树路径")
    branch: Optional[str] = Field(default=None, description="分支名")


class WorktreeInfo(BaseModel):
    path: str
    branch: str
    commit: str


class WorktreeOutput(BaseModel):
    success: bool
    worktrees: Optional[list] = None
    message: Optional[str] = None
    error: Optional[str] = None


def worktree_action(action: str, path: str = None, branch: str = None, cwd: str = ".") -> WorktreeOutput:
    """管理 Git Worktree"""
    try:
        if action == "list":
            result = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                cwd=cwd, capture_output=True, text=True
            )
            worktrees = []
            lines = result.stdout.strip().split('\n')
            current = {}
            for line in lines:
                if line.startswith("worktree "):
                    if current:
                        worktrees.append(current)
                    current = {"path": line[9:]}
                elif line.startswith("HEAD "):
                    current["commit"] = line[5:]
                elif line.startswith("branch "):
                    current["branch"] = line[7:]
            if current:
                worktrees.append(current)
            return WorktreeOutput(success=True, worktrees=worktrees)
        
        elif action == "create" and path and branch:
            subprocess.run(
                ["git", "worktree", "add", path, branch],
                cwd=cwd, capture_output=True, text=True, check=True
            )
            return WorktreeOutput(success=True, message=f"Created worktree at {path}")
        
        elif action == "remove" and path:
            subprocess.run(
                ["git", "worktree", "remove", path],
                cwd=cwd, capture_output=True, text=True, check=True
            )
            return WorktreeOutput(success=True, message=f"Removed worktree at {path}")
        
        return WorktreeOutput(success=False, error="Invalid action or missing parameters")
    except subprocess.CalledProcessError as e:
        return WorktreeOutput(success=False, error=e.stderr)
    except Exception as e:
        return WorktreeOutput(success=False, error=str(e))