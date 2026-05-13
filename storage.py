import json
import os
from collections import deque
from models import Task

class TaskHistory:
    """Управление очередью задач с сохранением в JSON"""

    def __init__(self, filename="tasks_history.json", max_size=100):
        self.filename = filename
        self.max_size = max_size
        self.queue = deque(maxlen=max_size)
        self.load_from_file()

    def add_task(self, task):
        """Добавить задачу в историю"""
        self.queue.append(task)
        self.save_to_file()

    def get_all_tasks(self):
        """Получить все задачи из истории"""
        return list(self.queue)

    def get_tasks_by_type(self, task_type):
        """Фильтрация по типу"""
        return [task for task in self.queue if task.type == task_type]

    def get_tasks_by_difficulty(self, difficulty):
        """Фильтрация по сложности"""
        return [task for task in self.queue if task.difficulty == difficulty]

    def clear_history(self):
        """Очистить историю"""
        self.queue.clear()
        self.save_to_file()

    def save_to_file(self):
        """Сохранить историю в JSON"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in self.queue], f,
                         ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load_from_file(self):
        """Загрузить историю из JSON"""
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.queue.clear()
                for task_dict in data:
                    self.queue.append(Task.from_dict(task_dict))
        except Exception as e:
            print(f"Ошибка загрузки: {e}")

    def __len__(self):
        return len(self.queue)
