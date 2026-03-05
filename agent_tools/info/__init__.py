# -*- coding: utf-8 -*-
"""
信息获取工具模块

参考: https://github.com/anomalyco/opencode/tree/main/packages/opencode/src/tool
"""
from .web_fetch import WebFetchInput, WebFetchOutput, fetch_web
from .web_search import WebSearchInput, WebSearchOutput, search_web

__all__ = [
    "WebFetchInput", "WebFetchOutput", "fetch_web",
    "WebSearchInput", "WebSearchOutput", "search_web",
]