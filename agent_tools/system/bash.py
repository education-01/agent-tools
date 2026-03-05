"""Bash 命令执行工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/bash.ts
"""
from pydantic import BaseModel, Field
from typing import Optional
import subprocess


class BashInput(BaseModel):
    """Bash 命令输入"""
    command: str = Field(description="要执行的命令")
    timeout: int = Field(default=30000, description="超时时间（毫秒）")
    cwd: Optional[str] = Field(default=None, description="工作目录")


class BashOutput(BaseModel):
    """Bash 命令输出"""
    stdout: str = Field(description="标准输出")
    stderr: str = Field(description="标准错误")
    exit_code: int = Field(description="退出码")
    success: bool = Field(description="是否成功")


def run_bash(command: str, timeout: int = 30000, cwd: str = None) -> BashOutput:
    """
    执行 Bash 命令
    
    参数:
        command: 要执行的命令
        timeout: 超时时间（毫秒）
        cwd: 工作目录
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout / 1000,
            cwd=cwd
        )
        
        return BashOutput(
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode,
            success=result.returncode == 0
        )
    except subprocess.TimeoutExpired:
        return BashOutput(
            stdout="",
            stderr=f"Command timed out after {timeout}ms",
            exit_code=-1,
            success=False
        )
    except Exception as e:
        return BashOutput(
            stdout="",
            stderr=str(e),
            exit_code=-1,
            success=False
        )