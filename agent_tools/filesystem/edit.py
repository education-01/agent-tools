"""文件编辑工具

参考: 
- https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/edit.ts
- https://github.com/cline/cline/blob/main/evals/diff-edits/diff-apply/diff-06-23-25.ts
- https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/utils/editCorrector.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional
import difflib


def normalize_line_endings(text: str) -> str:
    """规范化换行符 - 参考 OpenCode"""
    return text.replace('\r\n', '\n')


class EditInput(BaseModel):
    """编辑文件输入 - 参考 OpenCode edit.ts 参数"""
    file_path: str = Field(description="The absolute path to the file to modify")
    old_string: str = Field(description="The text to replace")
    new_string: str = Field(description="The text to replace it with (must be different from old_string)")
    replace_all: bool = Field(default=False, description="Replace all occurrences of old_string (default false)")


class EditOutput(BaseModel):
    """编辑文件输出"""
    success: bool = Field(description="Whether the edit was successful")
    path: str = Field(description="File path")
    replacements: int = Field(description="Number of replacements made")
    diff: Optional[str] = Field(default=None, description="Diff of changes")


def edit_file(file_path: str, old_string: str, new_string: str, replace_all: bool = False) -> EditOutput:
    """
    编辑文件内容 - 替换文本
    
    参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/edit.ts
    
    参数:
        file_path: 文件绝对路径
        old_string: 要替换的文本
        new_string: 替换后的文本
        replace_all: 替换所有匹配项
    """
    p = Path(file_path).expanduser().resolve()
    
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    
    if p.is_dir():
        raise ValueError(f"Path is a directory, not a file: {p}")
    
    # 参考 OpenCode 的检查
    if old_string == new_string:
        raise ValueError("No changes to apply: old_string and new_string are identical.")
    
    with open(p, 'r', encoding='utf-8') as f:
        content_old = f.read()
    
    # 规范化换行符
    content_old = normalize_line_endings(content_old)
    old_string_norm = normalize_line_endings(old_string)
    new_string_norm = normalize_line_endings(new_string)
    
    if old_string_norm not in content_old:
        # 参考 OpenCode 的错误提示
        return EditOutput(success=False, path=str(p), replacements=0)
    
    if replace_all:
        count = content_old.count(old_string_norm)
        content_new = content_old.replace(old_string_norm, new_string_norm)
    else:
        count = 1
        content_new = content_old.replace(old_string_norm, new_string_norm, 1)
    
    # 生成 diff - 参考 OpenCode 的 createTwoFilesPatch
    diff = ''.join(difflib.unified_diff(
        content_old.splitlines(keepends=True),
        content_new.splitlines(keepends=True),
        fromfile=str(p),
        tofile=str(p)
    ))
    
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content_new)
    
    return EditOutput(
        success=True,
        path=str(p),
        replacements=count,
        diff=diff
    )