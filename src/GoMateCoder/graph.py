from langgraph.graph import StateGraph,END
from .state import AgentState
from .nodes import agent_node,tools_node
from .router import should_continue

def build_graph():
    builder = StateGraph(AgentState)
    # 添加智能体节点
    builder.add_node("agent",agent_node)
    # 添加工具节点
    builder.add_node("tools",tools_node)
    # 设置起始点
    builder.set_entry_point("agent")
    # 设置条件边
    builder.add_conditional_edges("agent",should_continue,{
        "tools":"tools",
        "end":END
    })

    # 将点之间连接起来
    builder.add_edge("tools","agent")
    # 返回编译完成的图
    return builder.compile()