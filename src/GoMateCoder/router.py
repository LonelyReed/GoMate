from .state import AgentState

# 条件边判断
def should_continue(state:AgentState) -> str:
    """决定下一步应该进入哪一个节点"""
    last_message = state["messages"][-1]
    if hasattr(last_message,"tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"