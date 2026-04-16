from typing import Annotated,List,Literal
from langgraph.graph import add_messages
from typing_extensions import TypedDict

# 定义AI Agent的通用状态,继承自TypedDict
class AgentState(TypedDict):
    # message存储所有的对话历史和用户输入
    message:Annotated[list,add_messages]        # add_message将新的message追加到列表里面
    # 存储下一个要执行的结点名称，由结点内部决定，由路由函数读取，控制图的工作流向
    next:Literal["agent","tools","end"]         # 使用Literal限制了next的取值范围，保证类型安全