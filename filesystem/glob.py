"""文件系统 - Glob 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/glob.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/ls.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List


class GlobInput(BaseModel):
    pattern: str = Field(description="文件匹配模式，如 *.py")
    root_dir: Optional[str] = Field(default=".", description="搜索根目录")


class GlobOutput(BaseModel):
    success: bool
    files: Optional[List[str]] = None
    error: Optional[str] = None
    count: Optional[int] = None


def glob_files(pattern: str, root_dir: str = ".") -> GlobOutput:
    """匹配文件路径"""
    try:
        root = Path(root_dir).expanduser().resolve()
        if not root.exists():
            return GlobOutput(success=False, error=f"Directory not found: {root_dir}")
        
        files = [str(p.relative_to(root)) for p in root.glob(pattern)]
        files.sort()
        
        return GlobOutput(
            success=True,
            files=files,
            count=len(files)
        )
    except Exception as e:
        return GlobOutput(success=False, error=str(e))


if __name__ == "__main__":
    # 测试
    result = glob_files("*.py", "/home/admin/.openclaw/workspace/agent-tools")
    print(f"Success: {result.success}")
    print(f"Found {result.count} files: {result.files}")