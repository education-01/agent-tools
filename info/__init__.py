# -*- coding: utf-8 -*-
"""
Agent Tools - 信息获取工具

参考:
- https://github.com/anthropics/claude-code
- https://github.com/mariozechner/pi-coding-agent
"""
from .web_fetch import WebFetchInput, WebFetchOutput, fetch_web
from .web_search import WebSearchInput, WebSearchOutput, SearchResult, search_web

__all__ = [
    "WebFetchInput", "WebFetchOutput", "fetch_web",
    "WebSearchInput", "WebSearchOutput", "SearchResult", "search_web",
]