# LLM Memory

一个专为大语言模型设计的记忆管理系统，支持基于重要性的记忆筛选和持久化存储。

## 安装

```bash
pip install llm-memory
```
## 使用示例
```python 
from llm_memory import CombinedMemory

# 初始化记忆系统
memory = CombinedMemory(
    max_size=100,
    system_prompt="你是一个助手",
    uid="user123"
)

# 添加消息
memory.add_message("user", "你好", importance=1)
memory.add_message("assistant", "你好！有什么我可以帮你的吗？", importance=1)

# 获取上下文
context = memory.get_context()

# 保存到数据库
memory.save_memory_to_db()
```

## 特性
- 基于重要性的记忆管理
- 自动保持最近的对话
- 支持数据库持久化
- 可配置的系统提示词

5. 依赖文件 `requirements.txt`：


