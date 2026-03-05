"""用户提问工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/question.ts
"""
from pydantic import BaseModel, Field
from typing import Optional, List


# 参考 OpenCode 的 Question.Info
class Question(BaseModel):
    """问题 - 参考 OpenCode Question.Info"""
    question: str = Field(description="The question to ask")
    type: str = Field(default="text", description="Question type: text, select, multiselect")
    options: Optional[List[str]] = Field(default=None, description="Options for select/multiselect")


class AskInput(BaseModel):
    """提问输入 - 参考 OpenCode question.ts 参数"""
    questions: List[Question] = Field(description="Questions to ask")


class Answer(BaseModel):
    """回答"""
    question: str
    answer: List[str] = Field(default_factory=list)


class AskOutput(BaseModel):
    """提问输出"""
    success: bool = Field(description="是否成功")
    answers: List[Answer] = Field(description="用户回答")
    output: str = Field(description="Formatted output")


def ask_user(questions: List[Question]) -> AskOutput:
    """
    向用户提问
    
    参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/question.ts
    
    参数:
        questions: 问题列表
    """
    # 在实际使用时，这里会等待用户输入
    # 作为库函数，返回空答案，需要调用方填充
    answers = [
        Answer(question=q.question, answer=[])
        for q in questions
    ]
    
    # 参考 OpenCode 的格式化输出
    formatted = ', '.join([
        f'"{a.question}"="Unanswered"'
        for a in answers
    ])
    
    return AskOutput(
        success=True,
        answers=answers,
        output=f"User has answered your questions: {formatted}. You can now continue with the user's answers in mind."
    )