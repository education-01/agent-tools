# -*- coding: utf-8 -*-
"""
Agent Tools - 文件系统工具

参考实现:
- https://github.com/anthropics/claude-code (Claude Code Read/Write/Edit)
- https://github.com/mariozechner/pi-coding-agent (tool schema design)
- https://github.com/openai/openai-agents-python (tool patterns)
"""
from .read import ReadInput, ReadOutput, read_file
from .write import WriteInput, WriteOutput, write_file
from .edit import EditInput, EditOutput, edit_file
from .glob import GlobInput, GlobOutput, glob_files
from .grep import GrepInput, GrepOutput, grep_files, GrepMatch

__all__ = [
    "ReadInput", "ReadOutput", "read_file",
    "WriteInput", "WriteOutput", "write_file",
    "EditInput", "EditOutput", "edit_file",
    "GlobInput", "GlobOutput", "glob_files",
    "GrepInput", "GrepOutput", "grep_files", "GrepMatch",
]