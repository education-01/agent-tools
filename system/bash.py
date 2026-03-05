"""系统执行 - Bash 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/bash.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/bash.ts
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict
import subprocess
import os


class BashInput(BaseModel):
    command: str = Field(description="要执行的命令")
    timeout: Optional[int] = Field(default=30, description="超时时间（秒）")
    cwd: Optional[str] = Field(default=None, description="工作目录")
    env: Optional[Dict[str, str]] = Field(default=None, description="环境变量")


class BashOutput(BaseModel):
    success: bool
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None
    error: Optional[str] = None


def run_bash(command: str, timeout: int = 30, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None) -> BashOutput:
    """执行系统命令"""
    try:
        exec_env = os.environ.copy()
        if env:
            exec_env.update(env)
        
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            env=exec_env,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return BashOutput(
            success=result.returncode == 0,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode
        )
    except subprocess.TimeoutExpired:
        return BashOutput(success=False, error=f"Command timed out after {timeout}s", exit_code=-1)
    except Exception as e:
        return BashOutput(success=False, error=str(e))


if __name__ == "__main__":
    # 测试
    result = run_bash("echo 'Hello from bash' && ls -la ~/agent-tools", timeout=10)
    print(f"Success: {result.success}")
    print(f"Exit code: {result.exit_code}")
    print(f"Output: {result.stdout}")