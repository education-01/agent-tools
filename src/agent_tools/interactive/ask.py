"""用户交互 - Ask 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/askUser.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/askUser.ts
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class AskInput(BaseModel):
    question: str = Field(description="要问用户的问题")
    options: Optional[List[str]] = Field(default=None, description="选项列表（如果有）")


class AskOutput(BaseModel):
    question: str
    answer: Optional[str] = None
    pending: bool = True  # 标记是否需要用户回答


def ask_user(question: str, options: Optional[List[str]] = None) -> AskOutput:
    """向用户提问"""
    return AskOutput(
        question=question,
        pending=True
    )


# 注: 实际的用户回复处理需要在调用方实现
# 这个工具返回一个待回答的问题对象


if __name__ == "__main__":
    result = ask_user("你想做什么？", options=["写代码", "查资料", "聊天"])
    print(f"Question: {result.question}")
    print(f"Pending: {result.pending}")