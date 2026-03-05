"""网页搜索工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/websearch.ts
"""
from pydantic import BaseModel, Field
from typing import Optional, List
import re
import html
import urllib.request
import urllib.parse


class WebSearchResult(BaseModel):
    """搜索结果"""
    title: str
    url: str
    snippet: str


class WebSearchInput(BaseModel):
    """网页搜索输入"""
    query: str = Field(description="搜索关键词")
    count: int = Field(default=10, description="结果数量")


class WebSearchOutput(BaseModel):
    """网页搜索输出"""
    results: List[WebSearchResult] = Field(description="搜索结果")
    success: bool = Field(description="是否成功")
    error: Optional[str] = Field(default=None, description="错误信息")


def search_web(query: str, count: int = 10) -> WebSearchOutput:
    """
    搜索网页 - 使用 DuckDuckGo HTML 端点
    
    参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/websearch.ts
    
    参数:
        query: 搜索关键词
        count: 结果数量
    """
    try:
        url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; AgentTools/1.0)'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            text = response.read().decode('utf-8')
        
        # 解析搜索结果
        pattern = r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>'
        hits = re.findall(pattern, text)
        
        results = []
        for url, title in hits[:count]:
            # 清理 HTML 标签
            clean_title = re.sub('<[^>]+>', '', html.unescape(title)).strip()
            
            # 提取实际 URL (DuckDuckGo 使用重定向)
            if url.startswith('//'):
                url = 'https:' + url
            
            results.append(WebSearchResult(
                title=clean_title,
                url=url,
                snippet=""  # DuckDuckGo HTML 端点不提供 snippet
            ))
        
        if results:
            return WebSearchOutput(results=results, success=True)
        else:
            return WebSearchOutput(
                results=[],
                success=False,
                error="No search results found from DuckDuckGo."
            )
            
    except Exception as e:
        return WebSearchOutput(
            results=[],
            success=False,
            error=f"Search failed: {str(e)}"
        )
