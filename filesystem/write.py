"""文件系统 - Write 工具

参考实现:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/write.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/write.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional


class WriteInput(BaseModel):
    path: str = Field(description="文件路径")
    content: str = Field(description="写入内容")


class WriteOutput(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None
    bytes_written: Optional[int] = None


def write_file(path: str, content: str) -> WriteOutput:
    """写入文件内容"""
    try:
        p = Path(path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return WriteOutput(
            success=True,
            message=f"Successfully wrote {len(content)} bytes to {path}",
            bytes_written=len(content)
        )
    except Exception as e:
        return WriteOutput(success=False, error=str(e))


if __name__ == "__main__":
    # 测试
    result = write_file("/tmp/test_write.txt", "Hello from agent-tools!")
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")