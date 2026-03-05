"""高级 Agent 能力 - NotebookEdit 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/notebook.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/notebook.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List
import json


class NotebookCell(BaseModel):
    cell_type: str  # code, markdown
    source: str
    outputs: Optional[List[str]] = None


class NotebookEditInput(BaseModel):
    path: str = Field(description="Notebook 文件路径")
    cell_index: Optional[int] = Field(default=None, description="单元格索引")
    cell_type: Optional[str] = Field(default=None, description="单元格类型")
    source: Optional[str] = Field(default=None, description="单元格内容")
    new_source: Optional[str] = Field(default=None, description="新内容")


class NotebookOutput(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None


def edit_notebook(path: str, cell_index: int = None, cell_type: str = None, 
                  source: str = None, new_source: str = None) -> NotebookOutput:
    """编辑 Jupyter Notebook"""
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return NotebookOutput(success=False, error=f"Notebook not found: {path}")
        
        with open(p, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        if cell_index is not None and new_source:
            if 0 <= cell_index < len(nb.get('cells', [])):
                nb['cells'][cell_index]['source'] = new_source.split('\n')
        
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=2)
        
        return NotebookOutput(success=True, message=f"Updated cell {cell_index}")
    except Exception as e:
        return NotebookOutput(success=False, error=str(e))