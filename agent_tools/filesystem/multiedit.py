"""多重编辑工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/multiedit.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import List, Dict


class MultiEditItem(BaseModel):
    """单个编辑项"""
    old_string: str = Field(description="String to replace")
    new_string: str = Field(description="Replacement string")


class MultiEditInput(BaseModel):
    """多重编辑输入"""
    file_path: str = Field(description="The absolute path to the file to edit")
    edits: List[MultiEditItem] = Field(description="List of edits to apply in order")


class MultiEditOutput(BaseModel):
    """多重编辑输出"""
    success: bool = Field(description="Whether the edit was successful")
    file_path: str = Field(description="File path")
    applied: int = Field(description="Number of edits applied")
    total: int = Field(description="Total edits requested")
    message: str = Field(description="Result message")


def multi_edit(file_path: str, edits: List[Dict[str, str]]) -> MultiEditOutput:
    """
    在文件中应用多个字符串替换
    
    参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/multiedit.ts
    
    参数:
        file_path: 文件绝对路径
        edits: 编辑列表，每个包含 old_string 和 new_string
        
    返回:
        MultiEditOutput: 编辑结果
    """
    p = Path(file_path).expanduser().resolve()
    
    if not p.exists():
        return MultiEditOutput(
            success=False,
            file_path=str(p),
            applied=0,
            total=len(edits),
            message=f"File not found: {p}"
        )
    
    if not p.is_file():
        return MultiEditOutput(
            success=False,
            file_path=str(p),
            applied=0,
            total=len(edits),
            message=f"Not a file: {p}"
        )
    
    try:
        text = p.read_text(encoding='utf-8')
    except Exception as e:
        return MultiEditOutput(
            success=False,
            file_path=str(p),
            applied=0,
            total=len(edits),
            message=f"Failed to read file: {e}"
        )
    
    applied = 0
    for edit in edits:
        old_str = edit.get('old_string', '')
        new_str = edit.get('new_string', '')
        
        if old_str == new_str:
            continue
            
        if old_str in text:
            text = text.replace(old_str, new_str, 1)
            applied += 1
    
    try:
        p.write_text(text, encoding='utf-8')
    except Exception as e:
        return MultiEditOutput(
            success=False,
            file_path=str(p),
            applied=applied,
            total=len(edits),
            message=f"Failed to write file: {e}"
        )
    
    return MultiEditOutput(
        success=True,
        file_path=str(p),
        applied=applied,
        total=len(edits),
        message=f"Applied {applied}/{len(edits)} edits successfully"
    )
