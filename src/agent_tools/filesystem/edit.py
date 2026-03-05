"""文件系统 - Edit 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/edit.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/edit.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional


class EditInput(BaseModel):
    path: str = Field(description="文件路径")
    old_string: str = Field(description="要替换的旧文本")
    new_string: str = Field(description="新文本")


class EditOutput(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None
    replacements: Optional[int] = None


def edit_file(path: str, old_string: str, new_string: str) -> EditOutput:
    """编辑文件内容（替换指定文本）"""
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return EditOutput(success=False, error=f"File not found: {path}")
        
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_string not in content:
            return EditOutput(success=False, error="Old string not found in file")
        
        new_content = content.replace(old_string, new_string)
        replacements = content.count(old_string)
        
        with open(p, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return EditOutput(
            success=True,
            message=f"Replaced {replacements} occurrence(s)",
            replacements=replacements
        )
    except Exception as e:
        return EditOutput(success=False, error=str(e))


if __name__ == "__main__":
    # 测试
    result = edit_file("/tmp/test_edit.txt", "old", "new")
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")