"""信息获取 - WebFetch 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/webFetch.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/webFetch.ts
"""
from pydantic import BaseModel, Field
from typing import Optional
import requests


class WebFetchInput(BaseModel):
    url: str = Field(description="网页URL")
    max_chars: Optional[int] = Field(default=10000, description="最大字符数")
    verify_ssl: bool = Field(default=True, description="是否验证SSL证书")


class WebFetchOutput(BaseModel):
    success: bool
    content: Optional[str] = None
    title: Optional[str] = None
    error: Optional[str] = None


def fetch_web(url: str, max_chars: int = 10000, verify_ssl: bool = True) -> WebFetchOutput:
    """获取网页内容
    
    Args:
        url: 网页URL
        max_chars: 最大字符数
        verify_ssl: 是否验证SSL证书（默认True，某些环境可能需要关闭）
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30, verify=verify_ssl)
        response.raise_for_status()
        
        # 简单提取文本 - 移除 HTML 标签
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 移除 script 和 style
        for tag in soup(['script', 'style']):
            tag.decompose()
        
        text = soup.get_text(separator='\n', strip=True)
        
        # 截断
        if len(text) > max_chars:
            text = text[:max_chars] + f"\n... (truncated, total {len(text)} chars)"
        
        # 获取标题
        title = soup.title.string if soup.title else None
        
        return WebFetchOutput(
            success=True,
            content=text,
            title=title
        )
    except Exception as e:
        return WebFetchOutput(success=False, error=str(e))


if __name__ == "__main__":
    result = fetch_web("https://example.com")
    print(f"Success: {result.success}")
    if result.success:
        print(f"Title: {result.title}")
        print(f"Content: {result.content[:200]}...")