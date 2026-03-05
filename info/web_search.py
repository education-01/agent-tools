"""信息获取 - WebSearch 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/webSearch.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/webSearch.ts
"""
from pydantic import BaseModel, Field
from typing import Optional, List
import requests
from bs4 import BeautifulSoup
import urllib.parse


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str


class WebSearchInput(BaseModel):
    query: str = Field(description="搜索关键词")
    count: Optional[int] = Field(default=10, description="结果数量")


class WebSearchOutput(BaseModel):
    success: bool
    results: Optional[List[SearchResult]] = None
    error: Optional[str] = None


def search_web(query: str, count: int = 10, verify_ssl: bool = True) -> WebSearchOutput:
    """搜索网页 - 使用 DuckDuckGo
    
    Args:
        query: 搜索关键词
        count: 结果数量
        verify_ssl: 是否验证SSL证书
    """
    try:
        # 使用 DuckDuckGo HTML
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=30, verify=verify_ssl)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results: List[SearchResult] = []
        
        for result in soup.select('.result')[:count]:
            title_elem = result.select_one('.result__title')
            link_elem = result.select_one('.result__url')
            snippet_elem = result.select_one('.result__snippet')
            
            if title_elem:
                title = title_elem.get_text(strip=True)
                url = link_elem.get_text(strip=True) if link_elem else ""
                snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                
                results.append(SearchResult(
                    title=title,
                    url=url,
                    snippet=snippet
                ))
        
        return WebSearchOutput(
            success=True,
            results=results
        )
    except Exception as e:
        return WebSearchOutput(success=False, error=str(e))


if __name__ == "__main__":
    result = search_web("Python agent framework")
    print(f"Success: {result.success}")
    if result.success:
        for r in result.results[:3]:
            print(f"- {r.title}: {r.url}")