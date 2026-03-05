"""文件搜索工具 (Glob)

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/glob.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List


class GlobInput(BaseModel):
    """Glob 搜索输入"""
    pattern: str = Field(description="匹配模式 (如 **/*.py)")
    path: str = Field(default=".", description="搜索路径")


class GlobOutput(BaseModel):
    """Glob 搜索输出"""
    files: List[str] = Field(description="匹配的文件列表")
    count: int = Field(description="文件数量")


def glob_files(pattern: str, path: str = ".") -> GlobOutput:
    """
    使用 glob 模式搜索文件
    
    参数:
        pattern: 匹配模式 (如 **/*.py)
        path: 搜索起始路径
    """
    p = Path(path).expanduser().resolve()
    
    files = [str(f) for f in p.glob(pattern) if f.is_file()]
    
    return GlobOutput(
        files=files,
        count=len(files)
    )