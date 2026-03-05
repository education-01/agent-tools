"""文件读取工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/read.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List


class ReadInput(BaseModel):
    """读取文件输入"""
    file_path: str = Field(description="文件路径")
    offset: Optional[int] = Field(default=None, description="起始行号")
    limit: Optional[int] = Field(default=None, description="读取行数")


class ReadOutput(BaseModel):
    """读取文件输出"""
    content: str = Field(description="文件内容")
    lines: int = Field(description="总行数")
    path: str = Field(description="文件路径")


def read_file(file_path: str, offset: int = None, limit: int = None) -> ReadOutput:
    """
    读取文件内容
    
    参数:
        file_path: 文件路径
        offset: 起始行号（0-indexed）
        limit: 读取行数
    """
    p = Path(file_path).expanduser().resolve()
    
    if not p.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(p, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    
    if offset is not None:
        lines = lines[offset:]
    if limit is not None:
        lines = lines[:limit]
    
    return ReadOutput(
        content=''.join(lines),
        lines=total_lines,
        path=str(p)
    )