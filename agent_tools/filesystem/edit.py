"""文件编辑工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/edit.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional


class EditInput(BaseModel):
    """编辑文件输入"""
    file_path: str = Field(description="文件路径")
    old_text: str = Field(description="要替换的文本")
    new_text: str = Field(description="替换后的文本")
    replace_all: bool = Field(default=False, description="替换所有匹配")


class EditOutput(BaseModel):
    """编辑文件输出"""
    success: bool = Field(description="是否成功")
    path: str = Field(description="文件路径")
    replacements: int = Field(description="替换次数")


def edit_file(file_path: str, old_text: str, new_text: str, replace_all: bool = False) -> EditOutput:
    """
    编辑文件内容 - 替换文本
    
    参数:
        file_path: 文件路径
        old_text: 要替换的文本
        new_text: 替换后的文本
        replace_all: 替换所有匹配项
    """
    p = Path(file_path).expanduser().resolve()
    
    if not p.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_text not in content:
        return EditOutput(success=False, path=str(p), replacements=0)
    
    if replace_all:
        count = content.count(old_text)
        content = content.replace(old_text, new_text)
    else:
        count = 1
        content = content.replace(old_text, new_text, 1)
    
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return EditOutput(success=True, path=str(p), replacements=count)