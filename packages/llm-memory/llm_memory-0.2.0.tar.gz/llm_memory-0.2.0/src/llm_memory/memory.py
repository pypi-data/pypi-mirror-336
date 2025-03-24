from typing import List, Dict, Optional, Any
from tinydb import TinyDB, Query

class CombinedMemory:
    def __init__(self, system_prompt: Optional[str] = None, uid: Optional[str] = None, max_size: int, recent_size: int = 20, db_path: str = 'memory.json'):
        self.max_size = max_size
        self.recent_size = recent_size
        self.conversation_history: List[Dict[str, Any]] = []
        self.uid = uid
        self._db = TinyDB(db_path)
        
        if uid:
            self.load_memory_from_db()
        
        if not self.conversation_history and system_prompt:
            self.add_message("system", system_prompt, importance=10000)

    def add_message(self, role: str, content: str, importance: int = 1):
        message = {"role": role, "content": content, "importance": importance}
        self.conversation_history.append(message)

        if len(self.conversation_history) > self.max_size:
            recent = self.conversation_history[-self.recent_size:]
            older = self.conversation_history[:-self.recent_size]

            if older:
                sorted_older = sorted(older, key=lambda x: x["importance"], reverse=True)
                high_importance_messages = []
                importance_groups = []
                current_group = []
                current_importance = sorted_older[0]["importance"]
                for msg in sorted_older:
                    if msg["importance"] == current_importance:
                        current_group.append(msg)
                    else:
                        importance_groups.append(current_group)
                        current_group = [msg]
                        current_importance = msg["importance"]
                importance_groups.append(current_group)

                result = []
                space_left = self.max_size - len(recent)
                for group in importance_groups:
                    if len(result) + len(group) <= space_left:
                        result.extend(group)
                    else:
                        remaining_space = space_left - len(result)
                        result.extend(group[-remaining_space:])
                        break

                self.conversation_history = result + recent
            else:
                self.conversation_history = self.conversation_history[-self.max_size:]

    def get_context(self):
        return [{"role": msg["role"], "content": msg["content"]} for msg in self.conversation_history]

    def clear_memory(self):
        self.conversation_history = []
        
    def save_memory_to_db(self):
        if not self.uid:
            return
            
        User = Query()
        self._db.remove(User.uid == self.uid)
        
        self._db.insert({
            'uid': self.uid,
            'conversation_history': self.conversation_history,
            'timestamp': time.time()
        })
        
    def load_memory_from_db(self):
        if not self.uid:
            return
            
        User = Query()
        user_memory = self._db.get(User.uid == self.uid)
        if user_memory:
            self.conversation_history = user_memory.get('conversation_history', [])