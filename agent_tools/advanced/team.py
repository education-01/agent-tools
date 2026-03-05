"""团队协作工具

参考: https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import json
import urllib.request


# CU Cloud LLM 配置
CU_CLOUD_API_URL = "https://aigw-gzgy2.cucloud.cn:8443/v1/chat/completions"
CU_CLOUD_API_KEY = "sk-sp-buNehZIKmIakKQiryovaaP8bg8F8JINw"


class AgentRole(BaseModel):
    """代理角色"""
    name: str = Field(description="角色名称")
    task: str = Field(description="任务描述")


class TeamInput(BaseModel):
    """团队输入"""
    agents: List[AgentRole] = Field(description="代理角色列表")
    goal: str = Field(description="协作目标")


class TeamOutput(BaseModel):
    """团队输出"""
    success: bool = Field(description="是否成功")
    results: Optional[List[Dict[str, Any]]] = Field(default=None, description="各代理结果")
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


def collaborate(agents: List[AgentRole], goal: str) -> TeamOutput:
    """
    多代理协作
    
    参数:
        agents: 代理角色列表
        goal: 协作目标
    """
    results = []
    
    try:
        for agent in agents:
            prompt = f"""你是一个{agent.name}。
            
目标: {goal}

你的任务: {agent.task}

请完成你的任务并给出结果。"""
            
            result = call_llm(prompt)
            results.append({
                "agent": agent.name,
                "task": agent.task,
                "result": result
            })
        
        return TeamOutput(
            success=True,
            results=results
        )
    except Exception as e:
        return TeamOutput(
            success=False,
            error=str(e)
        )
