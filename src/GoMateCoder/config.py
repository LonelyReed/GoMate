from pydantic_settings import BaseSettings,SettingsConfigDict

# 定义一个setting类，继承BaseSettings

# 旧有语法，依然支持有效，此处试用新版语法
# class Settings(BaseSettings):
#     llm_api_key: str = ""
#     llm_name: str = "deepseek-chat"
#     worksapce_root: str = "."
#     command_timeout: int = 30

#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"

class Settings(BaseSettings):
    # 从环境变量加载配置
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding=".utf-8")

    # 配置初始化，集中管理
    model_api_key: str = ""
    model_name:str = "deepseek-chat"
    workspace_root:str = "."
    command_timeout:int = 30


settings = Settings()