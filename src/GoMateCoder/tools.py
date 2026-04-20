from langchain_core.tools import tool
from pathlib import Path        # python标准库Path类，实现路径操作
import subprocess               # 运行在沙箱环境
from .config import settings

# 辅助函数，校验路径是否合法，确保安全
def _safe_path(path:str) -> Path:           # 内部函数，被其他函数调用检查安全性
    """确保路径在工作区根目录WORKSPACE_ROOT，防止其他文件被篡改和路径遍历攻击"""
    full = (Path(settings.workspace_root)/path).resolve()
    root = Path(settings.workspace_root).resolve()

    if not str(full).startswith(str(root)):
        raise ValueError(f"请求取消：{path}路径访问越界")
    return full

# Agent工具函数

# 读取函数
@tool
def read_file(path:str) -> str:
    """读取工作区里面的文件"""
    try:
        return _safe_path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"错误：{path}没有找到"
    
# 写入函数
@tool
def write_file(path:str,content:str) -> str:
    """使用覆盖模型写入文件"""
    full = _safe_path(path)         # 安全限制
    full.parent.mkdir(parents=True,exist_ok=True)
    full.write_text(content,encoding="utf-8")

    return f"成功写入{len(content)}个字符到{path}"

# 执行函数
@tool
def run_command(command:str) -> str:
    """在工作区合理范围内执行shell命令，超时则限制执行"""
    try:
        result = subprocess.run(
            command,shell=True,cwd=settings.workspace_root,
            capture_output=True,text=True,timeout=settings.command_timeout
        )
        output = result.stdout + result.stderr
        if not output:
            output = "命令执行成功，没有输出"

        return output

    except subprocess.TimeoutExpired:
        return f"命令运行时间超过{settings.command_timeout}s"
    
# 创建工具列表，以便使用langgraph绑定到LLM上
TOOLS = [read_file,write_file,run_command]
# 构建字典，将工具名称对应到工具对象，以便通过工具名快速找到并执行对应工具
TOOLS_BY_NAME = {t.name : t for t in TOOLS}