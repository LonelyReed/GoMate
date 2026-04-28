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
            user_input = click.prompt("你",prompt_suffix="> ",type=str)                # 退出循环
            if user_input.strip() == "/exit":
                console.print("[bold red]成功退出GoMateCoder[/]")
                break

            # 将对话添加到历史
            messages.append(HumanMessage(content=user_input))
                
            # 流式输出回复，借助Live动态更新
            # 后续考虑采用io效率更高的异步处理
            with Live(refresh_per_second=4) as live:
                # 存储最终状态
                final_state = None
                # 流式输出图执行过程中的每个节点的输出
                for chunk in graph.stream({"messages":messages}):
                    # chunk是一个字典，其中key是节点名，value是该节点返回的状态更新
                    for node_name,state_update in chunk.items():
                        if "messages" in state_update:
                            # 获取最新的一条消息，可能来自于llm，或者是调用tool的输出
                            last_msg = state_update["messages"][-1]
                            if hasattr(last_msg,"content") and last_msg.content:
                                # 实时更新显示区
                                live.update(Markdown(last_msg.content))
                    # 记录最后的完整状态
                    final_state = state_update

                # 流式输出的循环结束后，将最终状态包含的消息合并到历史
                # 注意：graph.stream中，最后的状态包含了所有的新增信息
                if final_state and "messages" in final_state:
                    # 新消息是final_state["messages"]中哪些原先不在messages中的信息
                    # 这里偷懒，将messages直接更新为final_state
                    messages = final_state["messages"]

            # 进入下一轮对话
            console.print()

# 主函数，启动整个GoMateCoder
if __name__ == "__main__":
    main()