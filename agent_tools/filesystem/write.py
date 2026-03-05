"""文件写入工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/write.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional


class WriteInput(BaseModel):
    """写入文件输入 - 参考 OpenCode write.ts"""
    file_path: str = Field(description="The absolute path to the file to write")
    content: str = Field(description="The content to write to the file")


class WriteOutput(BaseModel):
    """写入文件输出"""
    success: bool = Field(description="Whether the write was successful")
    path: str = Field(description="File path")
    bytes_written: int = Field(description="Number of bytes written")


def write_file(file_path: str, content: str) -> WriteOutput:
    """
    写入文件内容
    
    参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/write.ts
    
    参数:
        file_path: 文件绝对路径
        content: 文件内容
    """
    p = Path(file_path).expanduser().resolve()
    
    # 创建父目录
    p.parent.mkdir(parents=True, exist_ok=True)
    
    # 规范化换行符 - 参考 OpenCode 的 normalizeLineEndings
    content = content.replace('\r\n', '\n')
    
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    
    return WriteOutput(
        success=True,
        path=str(p),
        bytes_written=len(content.encode('utf-8'))
    )