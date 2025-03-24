import unittest
from llm_memory import CombinedMemory

class TestCombinedMemory(unittest.TestCase):
    def setUp(self):
        self.memory = CombinedMemory(system_prompt=None, uid=None, max_size=5, recent_size=3)

    def test_add_message(self):
        self.memory.add_message("user", "Hello", importance=1)
        self.assertEqual(len(self.memory.get_context()), 1)

    def test_max_size(self):
        for i in range(10):
            self.memory.add_message("user", f"Message {i}", importance=1)
        self.assertEqual(len(self.memory.get_context()), 5)

    def test_recent_size(self):
        # 添加6条消息，max_size=5，recent_size=3
        for i in range(6):
            self.memory.add_message("user", f"Message {i}", importance=1)
        
        context = self.memory.get_context()
        # 验证总长度是否符合 max_size
        self.assertEqual(len(context), 5)
        # 验证最后3条消息是否保留（recent_size=3）
        self.assertEqual([msg["content"] for msg in context[-3:]], 
                        ["Message 3", "Message 4", "Message 5"])

    def test_clear_memory(self):
        self.memory.add_message("user", "Hello", importance=1)
        self.memory.clear_memory()
        self.assertEqual(len(self.memory.get_context()), 0)

if __name__ == '__main__':
    unittest.main()