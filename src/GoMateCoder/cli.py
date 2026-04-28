# 导入外部库
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
from langchain_core.messages import SystemMessage,HumanMessage

# 导入项目相关文件
from .graph import build_graph
from .prompts import SYSTEM_PROMPT
from .config import settings

# 创建全局控制台对象，用于强大的输出，而不是逊色的print
console = Console()

@click.command()                # 将函数变为CLI命令
@click.option('--task','-t',help="执行单次任务的具体描述，不提供则直接进入交互模式")        # 定义命令task
def main(task):
    """AI编程智能体GoMateCoder命令行入口"""
    # 构建langgraph图
    graph = build_graph()               #直接调用定义的类，返回的已经编译好的图

    if task:
        # 单次任务模式
        console.print(Panel("[bold cyan]GoMate[/]正在执行任务...",border_style="cyan"))
        # 构建初始信息列表，并注入系统提示词，添加task指令
        messages = [SystemMessage(content=SYSTEM_PROMPT),HumanMessage(content=task)]
        # 调用图graph，传入初始状态
        final_state = graph.invoke({"messages":messages})
        # 获取AI最近一次返回的消息
        last_message = final_state["messages"][-1]
        if hasattr(last_message,"content"):
            console.print(Markdown(last_message.content))

        else:
            # 交互式模式
            console.print(Panel.fit("[bold green]GoMateCoder[/]成功启动",border_style="green"))
            console.print("输入你的需求以及任务,[bold yellow]/exit[/] 退出\n")

            # 历史消息，注入系统提示词
            messages = [SystemMessage(content=SYSTEM_PROMPT)]

            # 交互循环
            while True:
                # 用户输入
                