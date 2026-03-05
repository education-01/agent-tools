"""Notebook 编辑工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class NotebookCell(BaseModel):
    """Notebook 单元格"""
    cell_type: str = Field(description="类型: code 或 markdown")
    source: str = Field(description="单元格内容")
    execution_count: Optional[int] = Field(default=None)


class NotebookInput(BaseModel):
    """Notebook 输入"""
    notebook_path: str = Field(description="Notebook 文件路径")
    cells: Optional[List[NotebookCell]] = Field(default=None, description="单元格列表")


class NotebookOutput(BaseModel):
    """Notebook 输出"""
    success: bool = Field(description="是否成功")
    path: str = Field(description="文件路径")
    error: Optional[str] = Field(default=None, description="错误信息")


def edit_notebook(notebook_path: str, cells: List[NotebookCell] = None) -> NotebookOutput:
    """
    编辑 Jupyter Notebook
    
    参数:
        notebook_path: Notebook 文件路径
        cells: 单元格列表
    """
    try:
        import json
        from pathlib import Path
        
        p = Path(notebook_path).expanduser().resolve()
        
        if not p.exists():
            # 创建新 notebook
            nb = {
                "cells": [],
                "metadata": {},
                "nbformat": 4,
                "nbformat_minor": 5
            }
        else:
            with open(p, 'r', encoding='utf-8') as f:
                nb = json.load(f)
        
        if cells:
            nb["cells"] = [
                {
                    "cell_type": c.cell_type,
                    "source": c.source.split('\n'),
                    "metadata": {},
                    "execution_count": c.execution_count
                }
                for c in cells
            ]
        
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=2)
        
        return NotebookOutput(success=True, path=str(p))
    except Exception as e:
        return NotebookOutput(success=False, path=notebook_path, error=str(e))