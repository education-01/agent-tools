"""LSP 代码理解工具

参考实现:
- https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/lsp.ts (OpenCode LSP)
- https://github.com/pappasam/jedi-language-server (Jedi LSP Server)
- https://microsoft.github.io/language-server-protocol/specification (LSP 协议规范)
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List, Any
from enum import Enum


# 参考 OpenCode 的操作列表
class LSPOperation(str, Enum):
    GO_TO_DEFINITION = "goToDefinition"
    FIND_REFERENCES = "findReferences"
    HOVER = "hover"
    DOCUMENT_SYMBOL = "documentSymbol"
    WORKSPACE_SYMBOL = "workspaceSymbol"
    GO_TO_IMPLEMENTATION = "goToImplementation"
    PREPARE_CALL_HIERARCHY = "prepareCallHierarchy"
    INCOMING_CALLS = "incomingCalls"
    OUTGOING_CALLS = "outgoingCalls"
    # 额外支持的 Jedi 操作
    COMPLETION = "completion"
    SIGNATURE_HELP = "signatureHelp"


class Position(BaseModel):
    """LSP Position 类型"""
    line: int = Field(description="行号（0-indexed）")
    character: int = Field(description="列号（0-indexed）")


class Range(BaseModel):
    """LSP Range 类型"""
    start: Position
    end: Position


class Location(BaseModel):
    """LSP Location 类型"""
    uri: str = Field(description="文件 URI")
    range: Range


class LSPInput(BaseModel):
    """LSP 输入 - 参考 OpenCode lsp.ts 参数"""
    operation: LSPOperation = Field(description="The LSP operation to perform")
    file_path: str = Field(description="The absolute or relative path to the file")
    line: int = Field(description="The line number (1-based, as shown in editors)")
    character: int = Field(description="The character offset (1-based, as shown in editors)")


class LSPOutput(BaseModel):
    """LSP 输出"""
    success: bool = Field(description="Whether the operation succeeded")
    result: Optional[List[Any]] = Field(default=None, description="Operation result")
    output: str = Field(description="Formatted output")
    error: Optional[str] = Field(default=None, description="Error message")


def lsp_request(
    operation: str,
    file_path: str,
    line: int,
    character: int
) -> LSPOutput:
    """
    LSP 代码理解
    
    参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/lsp.ts
    
    参数:
        operation: LSP 操作 (goToDefinition, findReferences, hover, documentSymbol, etc.)
        file_path: 文件路径
        line: 行号（1-based，与编辑器一致）
        character: 列号（1-based，与编辑器一致）
    """
    p = Path(file_path).expanduser().resolve()
    
    if not p.exists():
        return LSPOutput(
            success=False,
            output=f"File not found: {p}",
            error=f"File not found: {p}"
        )
    
    try:
        import jedi
    except ImportError:
        return LSPOutput(
            success=False,
            output="jedi not installed. Run: pip install jedi",
            error="jedi not installed"
        )
    
    # OpenCode 使用 1-based，Jedi 也使用 1-based 行号
    with open(p, 'r', encoding='utf-8') as f:
        source = f.read()
    
    script = jedi.Script(code=source, path=str(p))
    
    try:
        result = []
        
        if operation == "goToDefinition":
            defs = script.goto(line=line, column=character - 1)
            for d in defs:
                if d.module_path:
                    result.append({
                        "uri": str(d.module_path),
                        "range": {
                            "start": {"line": (d.line or 1) - 1, "character": d.column or 0},
                            "end": {"line": (d.line or 1) - 1, "character": (d.column or 0) + len(d.name)}
                        }
                    })
        
        elif operation == "findReferences":
            refs = script.get_references(line=line, column=character - 1)
            for r in refs:
                if r.module_path:
                    result.append({
                        "uri": str(r.module_path),
                        "range": {
                            "start": {"line": (r.line or 1) - 1, "character": r.column or 0},
                            "end": {"line": (r.line or 1) - 1, "character": (r.column or 0) + len(r.name)}
                        }
                    })
        
        elif operation == "hover":
            help_items = script.help(line=line, column=character - 1)
            for h in help_items:
                if h.docstring():
                    result.append({
                        "contents": h.docstring()
                    })
        
        elif operation == "documentSymbol":
            names = script.get_names()
            for name in names:
                result.append({
                    "name": name.name,
                    "kind": name.type,
                    "range": {
                        "start": {"line": (name.line or 1) - 1, "character": name.column or 0},
                        "end": {"line": (name.line or 1) - 1, "character": (name.column or 0) + len(name.name)}
                    }
                })
        
        elif operation == "completion":
            completions = script.complete(line=line, column=character - 1)
            for c in completions[:50]:
                result.append({
                    "label": c.name,
                    "kind": c.type,
                    "detail": c.description
                })
        
        else:
            return LSPOutput(
                success=False,
                output=f"Unsupported operation: {operation}",
                error=f"Unsupported operation: {operation}"
            )
        
        output = f"No results found for {operation}" if not result else str(result)
        
        return LSPOutput(
            success=True,
            result=result,
            output=output
        )
    
    except Exception as e:
        return LSPOutput(
            success=False,
            output=str(e),
            error=str(e)
        )