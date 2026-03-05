# -*- coding: utf-8 -*-
"""
文件系统工具模块

参考: https://github.com/anomalyco/opencode/tree/main/packages/opencode/src/tool
"""
from .read import ReadInput, ReadOutput, read_file
from .write import WriteInput, WriteOutput, write_file
from .edit import EditInput, EditOutput, edit_file
from .multiedit import MultiEditInput, MultiEditOutput, MultiEditItem, multi_edit
from .glob import GlobInput, GlobOutput, glob_files
from .grep import GrepInput, GrepOutput, grep_files

__all__ = [
    "ReadInput", "ReadOutput", "read_file",
    "WriteInput", "WriteOutput", "write_file",
    "EditInput", "EditOutput", "edit_file",
    "MultiEditInput", "MultiEditOutput", "MultiEditItem", "multi_edit",
    "GlobInput", "GlobOutput", "glob_files",
    "GrepInput", "GrepOutput", "grep_files",
]