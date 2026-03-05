"""文件读取工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/read.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List


# 参考 OpenCode 的常量
DEFAULT_READ_LIMIT = 2000
MAX_LINE_LENGTH = 2000
MAX_BYTES = 50 * 1024  # 50 KB


class ReadInput(BaseModel):
    """读取文件输入 - 参考 OpenCode read.ts 参数"""
    file_path: str = Field(description="The absolute path to the file or directory to read")
    offset: Optional[int] = Field(default=None, description="The line number to start reading from (1-indexed)")
    limit: Optional[int] = Field(default=None, description="The maximum number of lines to read (defaults to 2000)")


class ReadOutput(BaseModel):
    """读取文件输出"""
    content: str = Field(description="File content")
    lines: int = Field(description="Total lines")
    path: str = Field(description="File path")
    truncated: bool = Field(default=False, description="Whether output was truncated")


def read_file(file_path: str, offset: int = None, limit: int = None) -> ReadOutput:
    """
    读取文件内容
    
    参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/read.ts
    
    参数:
        file_path: 文件绝对路径
        offset: 起始行号（1-indexed，与 OpenCode 一致）
        limit: 读取行数（默认 2000）
    """
    p = Path(file_path).expanduser().resolve()
    
    if not p.exists():
        # 参考 OpenCode 的错误提示风格
        raise FileNotFoundError(f"File not found: {p}")
    
    if p.is_dir():
        # 目录列表 - 参考 OpenCode 的目录处理
        entries = list(p.iterdir())
        dirs = sorted([e.name + "/" for e in entries if e.is_dir()])
        files = sorted([e.name for e in entries if e.is_file()])
        content = "Directory listing:\n" + "\n".join(dirs + files)
        return ReadOutput(content=content, lines=len(dirs) + files.count("\n") + 1, path=str(p))
    
    with open(p, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    
    # OpenCode 使用 1-indexed offset
    start = (offset or 1) - 1
    if start < 0:
        start = 0
    
    end = start + (limit or DEFAULT_READ_LIMIT)
    selected_lines = lines[start:end]
    
    # 行截断 - 参考 OpenCode 的 MAX_LINE_LENGTH
    truncated_line = False
    for i, line in enumerate(selected_lines):
        if len(line) > MAX_LINE_LENGTH:
            selected_lines[i] = line[:MAX_LINE_LENGTH] + f"... (line truncated to {MAX_LINE_LENGTH} chars)\n"
            truncated_line = True
    
    content = ''.join(selected_lines)
    truncated = truncated_line or len(selected_lines) < total_lines - start
    
    # 字节限制 - 参考 OpenCode 的 MAX_BYTES
    if len(content.encode('utf-8')) > MAX_BYTES:
        content = content[:MAX_BYTES // 2] + f"\n... (truncated to {MAX_BYTES // 1024} KB)"
        truncated = True
    
    return ReadOutput(
        content=content,
        lines=total_lines,
        path=str(p),
        truncated=truncated
    )