"""文件写入工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/write.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional


class WriteInput(BaseModel):
    """写入文件输入"""
    file_path: str = Field(description="文件路径")
    content: str = Field(description="文件内容")


class WriteOutput(BaseModel):
    """写入文件输出"""
    success: bool = Field(description="是否成功")
    path: str = Field(description="文件路径")
    bytes_written: int = Field(description="写入字节数")


def write_file(file_path: str, content: str) -> WriteOutput:
    """
    写入文件内容
    
    参数:
        file_path: 文件路径
        content: 文件内容
    """
    p = Path(file_path).expanduser().resolve()
    
    # 创建父目录
    p.parent.mkdir(parents=True, exist_ok=True)
    
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return WriteOutput(
        success=True,
        path=str(p),
        bytes_written=len(content.encode('utf-8'))
    )