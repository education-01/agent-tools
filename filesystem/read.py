"""文件系统 - Read 工具

参考实现:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/read.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/read.ts
- https://github.com/openai/openai-agents-python/blob/main/src/agents/tools/file_tools.py
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional


class ReadInput(BaseModel):
    path: str = Field(description="文件路径")
    offset: Optional[int] = Field(default=0, description="起始偏移量（字节）")
    limit: Optional[int] = Field(default=None, description="最大读取字节数")


class ReadOutput(BaseModel):
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
    total_bytes: Optional[int] = None


def read_file(path: str, offset: int = 0, limit: Optional[int] = None) -> ReadOutput:
    """读取文件内容"""
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return ReadOutput(success=False, error=f"File not found: {path}")
        
        with open(p, 'r', encoding='utf-8') as f:
            f.seek(offset)
            if limit:
                content = f.read(limit)
            else:
                content = f.read()
        
        return ReadOutput(
            success=True,
            content=content,
            total_bytes=p.stat().st_size
        )
    except Exception as e:
        return ReadOutput(success=False, error=str(e))


if __name__ == "__main__":
    # 测试
    result = read_file("/home/admin/.openclaw/workspace/agent-tools/README.md")
    print(f"Success: {result.success}")
    if result.success:
        print(f"Content ({result.total_bytes} bytes): {result.content[:200]}...")
    else:
        print(f"Error: {result.error}")