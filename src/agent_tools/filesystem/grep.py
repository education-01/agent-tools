"""文件系统 - Grep 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/grep.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/grep.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List, Dict


class GrepInput(BaseModel):
    query: str = Field(description="搜索关键词")
    path: Optional[str] = Field(default=".", description="搜索路径")
    recursive: bool = Field(default=True, description="是否递归搜索")
    extension: Optional[str] = Field(default=None, description="文件扩展名过滤")


class GrepMatch(BaseModel):
    file: str
    line_number: int
    content: str


class GrepOutput(BaseModel):
    success: bool
    matches: Optional[List[GrepMatch]] = None
    error: Optional[str] = None
    total_matches: Optional[int] = None
    files_matched: Optional[int] = None


def grep_files(query: str, path: str = ".", recursive: bool = True, extension: Optional[str] = None) -> GrepOutput:
    """搜索文件内容"""
    try:
        root = Path(path).expanduser().resolve()
        if not root.exists():
            return GrepOutput(success=False, error=f"Path not found: {path}")
        
        matches: List[GrepMatch] = []
        
        if recursive:
            files = root.rglob(f"*.{extension}" if extension else "*")
        else:
            files = root.glob(f"*.{extension}" if extension else "*")
        
        for f in files:
            if not f.is_file():
                continue
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
                    for line_no, line in enumerate(fp, 1):
                        if query in line:
                            matches.append(GrepMatch(
                                file=str(f.relative_to(root)),
                                line_number=line_no,
                                content=line.rstrip()
                            ))
            except Exception:
                continue
        
        files_with_matches = len(set(m.file for m in matches))
        
        return GrepOutput(
            success=True,
            matches=matches,
            total_matches=len(matches),
            files_matched=files_with_matches
        )
    except Exception as e:
        return GrepOutput(success=False, error=str(e))


if __name__ == "__main__":
    # 测试
    result = grep_files("def ", "/home/admin/.openclaw/workspace/agent-tools/src")
    print(f"Success: {result.success}")
    print(f"Found {result.total_matches} matches in {result.files_matched} files")