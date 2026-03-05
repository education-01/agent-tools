"""子代理工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool
"""
from pydantic import BaseModel, Field
from typing import Optional, Any
import uuid
import json
import urllib.request


# CU Cloud LLM 配置
CU_CLOUD_API_URL = "https://aigw-gzgy2.cucloud.cn:8443/v1/chat/completions"
CU_CLOUD_API_KEY = "sk-sp-buNehZIKmIakKQiryovaaP8bg8F8JINw"


class AgentInput(BaseModel):
    """子代理输入"""
    prompt: str = Field(description="任务提示")
    model: Optional[str] = Field(default=None, description="模型名称")


class AgentOutput(BaseModel):
    """子代理输出"""
    success: bool = Field(description="是否成功")
    agent_id: str = Field(description="代理 ID")
    result: Optional[Any] = Field(default=None, description="执行结果")
    error: Optional[str] = Field(default=None, description="错误信息")


def call_llm(prompt: str, model: str = "glm-5") -> str:
    """调用 CU Cloud LLM"""
    try:
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        req = urllib.request.Request(
            CU_CLOUD_API_URL,
            data=json.dumps(data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {CU_CLOUD_API_KEY}'
            }
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
            
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {str(e)}")


def spawn_agent(prompt: str, model: str = None) -> AgentOutput:
    """
    生成子代理执行任务
    
    参数:
        prompt: 任务提示
        model: 可选的模型名称 (默认: glm-5)
    """
    agent_id = str(uuid.uuid4())[:8]
    
    try:
        result = call_llm(prompt, model or "glm-5")
        return AgentOutput(
            success=True,
            agent_id=agent_id,
            result=result
        )
    except Exception as e:
        return AgentOutput(
            success=False,
            agent_id=agent_id,
            error=str(e)
        )
