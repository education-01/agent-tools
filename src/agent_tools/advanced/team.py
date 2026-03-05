"""高级 Agent 能力 - Team Collaboration 工具

参考:
- https://github.com/anthropics/claude-code/blob/main/packages/claude-code/src/tools/team.ts
- https://github.com/mariozechner/pi-coding-agent/blob/main/src/core/tools/team.ts
"""
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional, List
import json
from datetime import datetime


class TeamMember(BaseModel):
    id: str
    name: str
    role: str = "member"


class TeamMessage(BaseModel):
    from_id: str
    to_id: Optional[str] = None
    content: str
    timestamp: str


class TeamCollabInput(BaseModel):
    action: str = Field(description="操作: create, join, leave, send, receive")
    team_id: Optional[str] = Field(default=None)
    member_name: Optional[str] = Field(default=None)
    message: Optional[str] = Field(default=None)
    to_member: Optional[str] = Field(default=None)


class TeamCollabOutput(BaseModel):
    success: bool
    team_id: Optional[str] = None
    members: Optional[List[TeamMember]] = None
    messages: Optional[List[TeamMessage]] = None
    error: Optional[str] = None


TEAM_FILE = Path.home() / ".agent_tools" / "teams.json"


def team_collab(action: str, team_id: str = None, member_name: str = None, 
                message: str = None, to_member: str = None) -> TeamCollabOutput:
    """团队协作工具"""
    try:
        if not TEAM_FILE.exists():
            teams = {}
        else:
            teams = json.loads(TEAM_FILE.read_text())
        
        if action == "create":
            new_id = f"team_{len(teams) + 1}"
            teams[new_id] = {
                "members": [],
                "messages": []
            }
            TEAM_FILE.parent.mkdir(parents=True, exist_ok=True)
            TEAM_FILE.write_text(json.dumps(teams, indent=2))
            return TeamCollabOutput(success=True, team_id=new_id)
        
        if not team_id or team_id not in teams:
            return TeamCollabOutput(success=False, error="Team not found")
        
        team = teams[team_id]
        
        if action == "join" and member_name:
            member = TeamMember(
                id=f"member_{len(team['members']) + 1}",
                name=member_name
            )
            team['members'].append(member.model_dump())
            TEAM_FILE.write_text(json.dumps(teams, indent=2))
            return TeamCollabOutput(
                success=True, 
                members=[TeamMember(**m) for m in team['members']]
            )
        
        if action == "send" and message:
            msg = TeamMessage(
                from_id=member_name or "unknown",
                to_id=to_member,
                content=message,
                timestamp=datetime.now().isoformat()
            )
            team['messages'].append(msg.model_dump())
            TEAM_FILE.write_text(json.dumps(teams, indent=2))
            return TeamCollabOutput(success=True)
        
        if action == "receive":
            messages = [TeamMessage(**m) for m in team['messages']]
            return TeamCollabOutput(success=True, messages=messages)
        
        return TeamCollabOutput(success=False, error="Invalid action")
    except Exception as e:
        return TeamCollabOutput(success=False, error=str(e))