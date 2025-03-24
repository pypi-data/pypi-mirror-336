LLM Memory

一个专为大语言模型设计的记忆管理系统，支持基于重要性的记忆筛选和持久化存储。

安装

使用以下命令安装：
pip install llm-memory

使用示例：

from llm_memory import CombinedMemory

# 初始化记忆系统
memory = CombinedMemory(
    system_prompt="你是一个助手",  # 系统提示词
    uid="user123",                # 用户ID，用于数据库存储
    max_size=100,                # 最大记忆容量
    recent_size=20               # 保留最近对话轮数
)

# 添加消息
memory.add_message("user", "你好", importance=1)
memory.add_message("assistant", "你好！有什么我可以帮你的吗？", importance=1)

# 获取上下文
context = memory.get_context()

# 保存到数据库
memory.save_memory_to_db()

参数说明：

- system_prompt: 系统提示词，可选
- uid: 用户唯一标识，用于数据库存储，可选
- max_size: 最大记忆容量，必需
- recent_size: 保留最近对话轮数，默认为20轮

特性：

- 基于重要性的记忆管理
- 自动保持最近的对话（可配置保留轮数）
- 支持数据库持久化
- 可配置的系统提示词

数据持久化：

当提供 uid 参数时，会自动将对话历史保存到本地数据库（使用 TinyDB）。数据库文件默认保存为 memory.json。

依赖：

Python >= 3.7
tinydb >= 4.7.0

许可证：

MIT License


