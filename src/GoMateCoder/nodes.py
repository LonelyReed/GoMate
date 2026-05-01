from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage,ToolMessage
from .state import AgentState
from .tools import TOOLS,TOOLS_BY_NAME
from .prompts import SYSTEM_PROMPT
from .config import settings

# 初始化模型并加载工具
llm = ChatDeepSeek(
    model = settings.model_name,
    api_key=settings.model_api_key,
    base_url=settings.model_url,
    temperature=0,
    reasoning_effort="max",                         # 设置思考强度
    extra_body={
        "thinking":{"type":"enabled"}               # 开启思考模式
    }
).bind_tools(TOOLS)

# 定义智能体节点
def agent_node(state:AgentState):
    """LLM决策节点：自主决定调用什么工具或者选择直接回答"""
    response = llm.invoke(state['messages'])

    return {"messages":[response]}

# 定义工具节点
def tools_node(state:AgentState):
    """执行工具调用节点"""
    # 最近一次的放回信息
    last_message = state['messages'][-1]
    results = []
    for tc in last_message.tool_calls:
        tool = TOOLS_BY_NAME[tc["name"]]
        result = tool.invoke(tc["args"])
        results.append(ToolMessage(content=str(result),tool_call_id=tc["id"]))

    return {"messages":results}