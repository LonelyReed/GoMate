from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage,ToolMessage
from .state import AgentState
from .tools import TOOLS,TOOLS_BY_NAME
from .prompts import SYSTEM_PROMPT
from .config import settings

# 初始化模型并加载工具
llm = ChatOpenAI(
    model = settings.model_name,
    api_key=settings.model_api_key,
).bind_tools(TOOLS)