"""用户提问工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/question.ts
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class AskInput(BaseModel):
    """提问输入"""
    question: str = Field(description="问题内容")
    options: Optional[List[str]] = Field(default=None, description="选项列表")


class AskOutput(BaseModel):
    """提问输出"""
    answer: str = Field(description="用户回答")
    question: str = Field(description="问题内容")


def ask_user(question: str, options: List[str] = None) -> AskOutput:
    """
    向用户提问并获取回答
    
    参数:
        question: 问题内容
        options: 可选的答案选项
    """
    # 在实际使用时，这里会等待用户输入
    # 作为库函数，返回一个需要处理的输出
    return AskOutput(
        answer="",  # 需要由调用方填充
        question=question
    )