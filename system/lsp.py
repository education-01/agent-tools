"""代码理解 - LSP 工具

参考实现:
- https://github.com/pappasam/jedi-language-server (Jedi LSP Server)
- https://github.com/microsoft/pyright (Python 静态类型检查)
- https://github.com/python-lsp/python-lsp-server (Python LSP Server)
- https://microsoft.github.io/language-server-protocol/specification (LSP 协议规范)

基于:
- jedi: Python 代码分析
- lsprotocol: LSP 协议类型
- pygls: Python LSP 服务器框架
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum


class LSPAction(str, Enum):
    DEFINITION = "definition"
    REFERENCES = "references"
    HOVER = "hover"
    COMPLETION = "completion"
    RENAME = "rename"
    DOCUMENT_SYMBOL = "document_symbol"
    SIGNATURE_HELP = "signature_help"


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


class CompletionItemKind(int, Enum):
    """LSP CompletionItemKind"""
    TEXT = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCTOR = 4
    FIELD = 5
    VARIABLE = 6
    CLASS = 7
    INTERFACE = 8
    MODULE = 9
    PROPERTY = 10
    KEYWORD = 14


class SymbolKind(int, Enum):
    """LSP SymbolKind - 参考 https://microsoft.github.io/language-server-protocol/specification"""
    FILE = 1
    MODULE = 2
    NAMESPACE = 3
    PACKAGE = 4
    CLASS = 5
    METHOD = 6
    PROPERTY = 7
    FIELD = 8
    FUNCTION = 12
    VARIABLE = 13


class CompletionItem(BaseModel):
    """LSP CompletionItem 类型"""
    label: str
    kind: Optional[CompletionItemKind] = None
    detail: Optional[str] = None
    documentation: Optional[str] = None
    insert_text: Optional[str] = None


class DocumentSymbol(BaseModel):
    """LSP DocumentSymbol 类型"""
    name: str
    kind: SymbolKind
    range: Range
    selection_range: Range
    detail: Optional[str] = None
    children: Optional[List["DocumentSymbol"]] = None


class SignatureInformation(BaseModel):
    """LSP SignatureInformation 类型"""
    label: str
    documentation: Optional[str] = None
    parameters: Optional[List[str]] = None


class MarkupContent(BaseModel):
    """LSP MarkupContent 类型"""
    kind: str = "markdown"
    value: str


class LSPInput(BaseModel):
    """LSP 工具输入"""
    action: LSPAction = Field(description="LSP 操作类型")
    file_path: str = Field(description="文件路径")
    position: Optional[Position] = Field(default=None, description="光标位置")
    new_name: Optional[str] = Field(default=None, description="新名称（用于 rename）")


class LSPOutput(BaseModel):
    """LSP 工具输出"""
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None


# 类型映射：Jedi -> LSP
_JEDI_TO_LSP_KIND = {
    "module": CompletionItemKind.MODULE,
    "class": CompletionItemKind.CLASS,
    "instance": CompletionItemKind.CLASS,
    "function": CompletionItemKind.FUNCTION,
    "param": CompletionItemKind.VARIABLE,
    "path": CompletionItemKind.TEXT,
    "keyword": CompletionItemKind.KEYWORD,
    "property": CompletionItemKind.PROPERTY,
    "statement": CompletionItemKind.VARIABLE,
}

_JEDI_TO_SYMBOL_KIND = {
    "module": SymbolKind.MODULE,
    "class": SymbolKind.CLASS,
    "instance": SymbolKind.CLASS,
    "function": SymbolKind.FUNCTION,
    "param": SymbolKind.VARIABLE,
    "path": SymbolKind.FILE,
    "statement": SymbolKind.VARIABLE,
}


def _jedi_name_to_location(name) -> Optional[Location]:
    """将 Jedi Name 转换为 LSP Location"""
    if not name.module_path:
        return None
    return Location(
        uri=str(name.module_path),
        range=Range(
            start=Position(line=(name.line or 1) - 1, character=(name.column or 0)),
            end=Position(line=(name.line or 1) - 1, character=(name.column or 0) + len(name.name))
        )
    )


def _jedi_completion_to_item(completion) -> CompletionItem:
    """将 Jedi Completion 转换为 LSP CompletionItem"""
    kind = _JEDI_TO_LSP_KIND.get(completion.type, CompletionItemKind.TEXT)
    return CompletionItem(
        label=completion.name,
        kind=kind,
        detail=completion.description,
        documentation=completion.docstring()[:500] if completion.docstring() else None,
        insert_text=completion.name
    )


def _get_script(file_path: str):
    """获取 Jedi Script 对象"""
    try:
        import jedi
    except ImportError:
        raise ImportError("jedi not installed. Run: pip install jedi")
    
    p = Path(file_path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(p, 'r', encoding='utf-8') as f:
        source = f.read()
    
    return jedi.Script(code=source, path=str(p)), p


def lsp_definition(file_path: str, line: int, character: int) -> LSPOutput:
    """跳转到定义 - textDocument/definition"""
    try:
        script, p = _get_script(file_path)
        # Jedi 使用 1-indexed 行号
        definitions = script.goto(line=line + 1, column=character)
        
        results = []
        for d in definitions:
            loc = _jedi_name_to_location(d)
            if loc:
                results.append(loc.model_dump())
        
        return LSPOutput(success=True, result=results)
    except Exception as e:
        return LSPOutput(success=False, error=str(e))


def lsp_references(file_path: str, line: int, character: int) -> LSPOutput:
    """查找引用 - textDocument/references"""
    try:
        script, p = _get_script(file_path)
        references = script.get_references(line=line + 1, column=character)
        
        results = []
        for r in references:
            loc = _jedi_name_to_location(r)
            if loc:
                results.append(loc.model_dump())
        
        return LSPOutput(success=True, result=results)
    except Exception as e:
        return LSPOutput(success=False, error=str(e))


def lsp_hover(file_path: str, line: int, character: int) -> LSPOutput:
    """悬停提示 - textDocument/hover"""
    try:
        script, p = _get_script(file_path)
        help_items = script.help(line=line + 1, column=character)
        
        if not help_items:
            return LSPOutput(success=True, result=None)
        
        contents = []
        for h in help_items:
            docstring = h.docstring()
            if docstring:
                contents.append(f"**{h.name}**\n\n```python\n{docstring}\n```")
        
        if contents:
            return LSPOutput(
                success=True,
                result=MarkupContent(kind="markdown", value="\n\n---\n\n".join(contents)).model_dump()
            )
        return LSPOutput(success=True, result=None)
    except Exception as e:
        return LSPOutput(success=False, error=str(e))


def lsp_completion(file_path: str, line: int, character: int) -> LSPOutput:
    """代码补全 - textDocument/completion"""
    try:
        script, p = _get_script(file_path)
        completions = script.complete(line=line + 1, column=character)
        
        results = []
        for c in completions[:100]:  # 限制数量
            results.append(_jedi_completion_to_item(c).model_dump())
        
        return LSPOutput(success=True, result=results)
    except Exception as e:
        return LSPOutput(success=False, error=str(e))


def lsp_signature_help(file_path: str, line: int, character: int) -> LSPOutput:
    """签名帮助 - textDocument/signatureHelp"""
    try:
        script, p = _get_script(file_path)
        signatures = script.get_signatures(line=line + 1, column=character)
        
        if not signatures:
            return LSPOutput(success=True, result=None)
        
        results = []
        for sig in signatures:
            params = [p.name for p in sig.params] if sig.params else []
            results.append(SignatureInformation(
                label=sig.name,
                documentation=sig.docstring()[:500] if sig.docstring() else None,
                parameters=params
            ).model_dump())
        
        return LSPOutput(success=True, result=results)
    except Exception as e:
        return LSPOutput(success=False, error=str(e))


def lsp_document_symbol(file_path: str) -> LSPOutput:
    """文档符号 - textDocument/documentSymbol"""
    try:
        script, p = _get_script(file_path)
        names = script.get_names()
        
        results = []
        for name in names:
            kind = _JEDI_TO_SYMBOL_KIND.get(name.type, SymbolKind.VARIABLE)
            results.append(DocumentSymbol(
                name=name.name,
                kind=kind,
                range=Range(
                    start=Position(line=(name.line or 1) - 1, character=(name.column or 0)),
                    end=Position(line=(name.line or 1) - 1, character=(name.column or 0) + len(name.name))
                ),
                selection_range=Range(
                    start=Position(line=(name.line or 1) - 1, character=(name.column or 0)),
                    end=Position(line=(name.line or 1) - 1, character=(name.column or 0) + len(name.name))
                ),
                detail=name.description
            ).model_dump())
        
        return LSPOutput(success=True, result=results)
    except Exception as e:
        return LSPOutput(success=False, error=str(e))


def lsp_request(
    action: str,
    file_path: str,
    line: int = 0,
    column: int = 0,
    new_name: str = None
) -> LSPOutput:
    """
    LSP 工具 - 提供代码理解能力
    
    参考:
    - https://github.com/pappasam/jedi-language-server
    - https://microsoft.github.io/language-server-protocol/specification
    
    参数:
        action: LSP 操作 (definition, references, hover, completion, signature_help, document_symbol)
        file_path: 文件路径
        line: 行号 (0-indexed, LSP 标准)
        column: 列号 (0-indexed, LSP 标准)
        new_name: 新名称（用于 rename，暂未实现）
    
    返回:
        LSPOutput: 包含 LSP 协议标准的结果
    """
    action_map = {
        "definition": lambda: lsp_definition(file_path, line, column),
        "references": lambda: lsp_references(file_path, line, column),
        "hover": lambda: lsp_hover(file_path, line, column),
        "completion": lambda: lsp_completion(file_path, line, column),
        "signature_help": lambda: lsp_signature_help(file_path, line, column),
        "document_symbol": lambda: lsp_document_symbol(file_path),
    }
    
    if action not in action_map:
        return LSPOutput(success=False, error=f"Unknown action: {action}. Available: {list(action_map.keys())}")
    
    return action_map[action]()


if __name__ == "__main__":
    import sys
    
    # 测试
    file_path = __file__
    
    print("=== 测试 LSP 工具 ===\n")
    
    # 1. 补全
    print("1. Completion (line 0, column 0):")
    result = lsp_request("completion", file_path, 0, 0)
    if result.success:
        print(f"   Found {len(result.result)} items")
        for item in result.result[:5]:
            print(f"   - {item['label']} (kind={item['kind']})")
    
    # 2. 文档符号
    print("\n2. Document Symbols:")
    result = lsp_request("document_symbol", file_path)
    if result.success:
        print(f"   Found {len(result.result)} symbols")
        for sym in result.result[:5]:
            print(f"   - {sym['name']} (kind={sym['kind']})")
    
    # 3. 悬停
    print("\n3. Hover (line 50, column 5):")
    result = lsp_request("hover", file_path, 50, 5)
    if result.success and result.result:
        print(f"   {result.result['value'][:200]}...")
    else:
        print(f"   No hover info")
