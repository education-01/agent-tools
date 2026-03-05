"""网页抓取工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/webfetch.ts
"""
from pydantic import BaseModel, Field
from typing import Optional
import urllib.request
import urllib.error


class WebFetchInput(BaseModel):
    """网页抓取输入"""
    url: str = Field(description="要抓取的 URL")
    max_chars: int = Field(default=10000, description="最大字符数")


class WebFetchOutput(BaseModel):
    """网页抓取输出"""
    content: str = Field(description="网页内容")
    url: str = Field(description="URL")
    success: bool = Field(description="是否成功")
    error: Optional[str] = Field(default=None, description="错误信息")


def fetch_web(url: str, max_chars: int = 10000) -> WebFetchOutput:
    """
    抓取网页内容
    
    参数:
        url: 要抓取的 URL
        max_chars: 最大字符数
    """
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; AgentTools/1.0)'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8', errors='replace')
            
            # 简单提取文本内容
            # 移除 script 和 style 标签
            import re
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
            content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
            # 移除 HTML 标签
            content = re.sub(r'<[^>]+>', ' ', content)
            # 清理空白
            content = re.sub(r'\s+', ' ', content).strip()
            
            if len(content) > max_chars:
                content = content[:max_chars] + '...'
            
            return WebFetchOutput(
                content=content,
                url=url,
                success=True
            )
    except urllib.error.URLError as e:
        return WebFetchOutput(
            content="",
            url=url,
            success=False,
            error=str(e)
        )
    except Exception as e:
        return WebFetchOutput(
            content="",
            url=url,
            success=False,
            error=str(e)
        )