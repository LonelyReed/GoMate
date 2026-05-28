import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel,Field
import subprocess
import json

load_dotenv()

# 生成Schema,提供工具给大模型
class ShellCommand(BaseModel):
    """Parameters for executing a shell command"""
    command:str = Field(description="The shell command to execute. e.g.,'ls -la','mkdir test'")

# 定义工具格式
tools = [
    {
        "type":"function",
        "function":{
            "name":"shell",
            "description":"Execute a shell command.Use this to run terminal command.",
            "parameters":ShellCommand.model_json_schema()
        }
    }
]

# 定义工具
def execute_shell(command:str) -> str:
    """Execute a shell command and return stdout + stderr."""
   
    # 命令请求
    confirm = input(f"#{command}# Whether to execute[y/n]: ")
    if confirm.lower() not in ['y','Y']:
        return "The user rejected the command execution request"
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            encoding="utf-8",               # 使用utf-8解码
            errors="replace",               # 遇到无法解码的字符用其他字符替代
            timeout=30
        )
        return result.stdout + result.stderr
      
    except Exception as e:
        return f"Error executing command:{str(e)}"


# 模型基本属性
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API"),
    base_url=os.getenv("DEEPSEEK_URL")
)

# TAOR循环
def agent_loop(user_message:str):
    messages=[
                {"role":"system","content":"你是一个有用的助手，语言风格幽默风趣"},
                {"role":"user","content":user_message}
            ]

    # 循环
    while True:

        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME","deepseek-v4-flash"),
            messages=messages,
            tools=tools,
            stream=False
        )
        
        assistant_msg = response.choices[0].message

        # 如果没有工具调用，循环结束，返回大模型文本内容
        if not assistant_msg.tool_calls:
            return assistant_msg.content
        
        # 将助手信息加入历史，包含工具调用信息tool_call
        messages.append(assistant_msg)

        # 逐一执行工具调用，并追加结果
        for tool_call in assistant_msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "shell":
                result = execute_shell(args["command"])
            else:
                result = "Unknown tool"
        
        messages.append({
            "role":"tool",
            "tool_call_id":tool_call.id,
            "content":result,
        })

def main():
    print("###GoMate-owl###")
    while True:
        user_input = input("你：")
        if user_input.lower() in ["exit","quit","退出"]:
            break

        if not user_input.strip():
            continue

        print("thinking...",flush=True)

        try:
            result = agent_loop(user_input)
            print(f"AI: {result}")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()