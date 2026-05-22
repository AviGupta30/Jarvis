from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict
from app.services.tools import TOOL_REGISTRY

router = APIRouter()

class ToolExecuteRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = {}

@router.post("/execute")
async def execute_tool(request: ToolExecuteRequest):
    if request.tool_name not in TOOL_REGISTRY:
        return {
            "status": "denied",
            "output": "Sorry, I do not have access for this function or the request was disallowed."
        }
    
    try:
        func = TOOL_REGISTRY[request.tool_name]
        result = func(**request.arguments)
        return {
            "status": "success",
            "output": result
        }
    except Exception:
        return {
            "status": "denied",
            "output": "Sorry, I do not have access for this function or the request was disallowed."
        }
