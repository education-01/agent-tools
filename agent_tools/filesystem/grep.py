"""文件内容搜索工具 (Grep)

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/grep.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List
import re


class GrepInput(BaseModel):
    """Grep 搜索输入"""
    pattern: str = Field(description="搜索模式 (正则表达式)")
    path: str = Field(default=".", description="搜索路径")
    file_pattern: str = Field(default="*", description="文件匹配模式")


class GrepMatch(BaseModel):
    """匹配结果"""
    file: str
    line: int
    content: str


class GrepOutput(BaseModel):
    """Grep 搜索输出"""
    matches: List[GrepMatch] = Field(description="匹配列表")
    count: int = Field(description="匹配数量")


def grep_files(pattern: str, path: str = ".", file_pattern: str = "*") -> GrepOutput:
    """
    在文件中搜索匹配的内容
    
    参数:
        pattern: 搜索模式 (正则表达式)
        path: 搜索路径
        file_pattern: 文件匹配模式 (如 *.py)
    """
    p = Path(path).expanduser().resolve()
    regex = re.compile(pattern)
    matches = []
    
    for file_path in p.rglob(file_pattern):
        if not file_path.is_file():
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    if regex.search(line):
                        matches.append(GrepMatch(
                            file=str(file_path),
                            line=i,
                            content=line.rstrip()
                        ))
        except Exception:
            continue
    
    return GrepOutput(
        matches=matches,
        count=len(matches)
    )