"""Bash 命令执行工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/bash.ts
"""
from pydantic import BaseModel, Field
from typing import Optional
import subprocess


# 参考 OpenCode 的常量
DEFAULT_TIMEOUT = 2 * 60 * 1000  # 2 分钟


class BashInput(BaseModel):
    """Bash 命令输入 - 参考 OpenCode bash.ts 参数"""
    command: str = Field(description="The command to execute")
    timeout: Optional[int] = Field(default=None, description="Optional timeout in milliseconds")
    workdir: Optional[str] = Field(default=None, description="The working directory to run the command in")
    description: Optional[str] = Field(
        default=None,
        description="Clear, concise description of what this command does in 5-10 words"
    )


class BashOutput(BaseModel):
    """Bash 命令输出"""
    stdout: str = Field(description="Standard output")
    stderr: str = Field(description="Standard error")
    exit_code: int = Field(description="Exit code")
    success: bool = Field(description="Whether the command succeeded")
    interrupted: bool = Field(default=False, description="Whether the command was interrupted")


def run_bash(
    command: str,
    timeout: int = None,
    workdir: str = None,
    description: str = None
) -> BashOutput:
    """
    执行 Bash 命令
    
    参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/bash.ts
    
    参数:
        command: 要执行的命令
        timeout: 超时时间（毫秒），默认 2 分钟
        workdir: 工作目录
        description: 命令描述（5-10 个词）
    """
    timeout_ms = timeout or DEFAULT_TIMEOUT
    timeout_sec = timeout_ms / 1000
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            cwd=workdir
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
            stderr=f"Command timed out after {timeout_ms}ms",
            exit_code=-1,
            success=False,
            interrupted=True
        )
    except Exception as e:
        return BashOutput(
            stdout="",
            stderr=str(e),
            exit_code=-1,
            success=False
        )