"""
GoMate,一个基于langchain和langgraph构建的适配于deepseek的AI编程智能体
"""

# 版本
__version__ = "0.1.0" 

# 对外接口
from .cli import main
from .config import settings
from .graph import build_graph
from .tools import TOOLS

__all__ = ["main","settings","build_graph","TOOLS"]