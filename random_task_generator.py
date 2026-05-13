import json
import random
import os
from collections import deque
from abc import ABC, abstractmethod

# ------------------ Модель задачи ------------------
class Task:
    """Модель задачи (базовый класс)"""
    def __init__(self, description, task_type, difficulty):
        self._description = description  # инкапсуляция
        self._type = task_type
        self._difficulty = difficulty

    # Геттеры
    @property
    def description(self):
        return self._description

    @property
    def type(self):
        return self._type

    @property
    def difficulty(self):
        return self._difficulty

    # Сеттеры с валидацией
    @description.setter
    def description(self, value):
        if value and isinstance(value, str):
            self._description = value
        else:
            raise ValueError("Описание должно быть непустой строкой")

    @difficulty.setter
    def difficulty(self, value):
        if value in [1, 2, 3, 4, 5]:
            self._difficulty = value
        else:
            raise ValueError("Сложность должна быть от 1 до 5")

    def to_dict(self):
        """Конвертация в словарь для JSON"""
        return {
            'description': self._description,
            'type': self._type,
            'difficulty': self._difficulty
        }

    @classmethod
    def from_dict(cls, data):
        """Создание задачи из словаря"""
        return cls(data['description'], data['type'], data['difficulty'])

    def __str__(self):
        difficulties = {1: "★☆☆☆☆", 2: "★★☆☆☆", 3: "★★★☆☆", 4: "★★★★☆", 5: "★★★★★"}
        return f"[{self._type}] {self._description} (Сложность: {difficulties.get(self._difficulty, '?')})"


# ------------------ Конкретные типы задач ------------------
class WorkTask(Task):
    """Рабочая задача"""
    def __init__(self, description, difficulty):
        super().__init__(description, "Работа", difficulty)


class SportTask(Task):
    """Спортивная задача"""
    def __init__(self, description, difficulty):
        super().__init__(description, "Спорт", difficulty)


class StudyTask(Task):
    """Учебная задача"""
    def __init__(self, description, difficulty):
        super().__init__(description, "Учеба", difficulty)


class HomeTask(Task):
    """Домашняя задача"""
    def __init__(self, description, difficulty):
        super().__init__(description, "Дом", difficulty)


class HobbyTask(Task):
    """Хобби задача"""
    def __init__(self, description, difficulty):
        super().__init__(description, "Хобби", difficulty)


# ------------------ Фабрика задач (паттерн Factory) ------------------
class TaskFactory:
    """Фабрика для создания задач разных типов"""

    _task_types = {
        "Работа": WorkTask,
        "Спорт": SportTask,
        "Учеба": StudyTask,
        "Дом": HomeTask,
        "Хобби": HobbyTask
    }

    # Предопределенные задачи по типам
    _task_templates = {
        "Работа": [
            ("Закончить отчет", 3),
            ("Провести совещание", 2),
            ("Ответить на письма", 1),
            ("Подготовить презентацию", 4),
            ("Сделать код-ревью", 3),
            ("Написать документацию", 2),
            ("Созвониться с клиентом", 2),
            ("Планирование задач", 1)
        ],
        "Спорт": [
            ("Пробежка 5 км", 3),
            ("Тренировка в зале", 4),
            ("Йога 30 минут", 2),
            ("Отжимания 50 раз", 3),
            ("Плавание", 3),
            ("Велосипедная прогулка", 2),
            ("Растяжка", 1),
            ("Комплекс упражнений", 4)
        ],
        "Учеба": [
            ("Прочитать 20 страниц", 2),
            ("Решить задачи", 4),
            ("Посмотреть лекцию", 2),
            ("Выучить 10 новых слов", 3),
            ("Сделать конспект", 2),
            ("Пройти тест", 3),
            ("Написать эссе", 4),
            ("Изучить новую тему", 4)
        ],
        "Дом": [
            ("Убрать комнату", 2),
            ("Приготовить ужин", 3),
            ("Помыть посуду", 1),
            ("Стирка", 2),
            ("Полить цветы", 1),
            ("Вынести мусор", 1),
            ("Пропылесосить", 2),
            ("Протереть пыль", 1)
        ],
        "Хобби": [
            ("Поиграть на гитаре", 3),
            ("Нарисовать картину", 4),
            ("Почитать книгу", 2),
            ("Собрать пазл", 3),
            ("Посмотреть фильм", 1),
            ("Сделать поделку", 4),
            ("Написать рассказ", 3),
            ("Потанцевать", 2)
        ]
    }

    @classmethod
    def create_task(cls, task_type, description=None, difficulty=None):
        """Создание задачи заданного типа"""
        if task_type not in cls._task_types:
            raise ValueError(f"Неизвестный тип задачи: {task_type}")

        task_class = cls._task_types[task_type]

        # Если описание не указано, генерируем случайную задачу этого типа
        if description is None:
            templates = cls._task_templates.get(task_type, [])
            if templates:
                description, difficulty = random.choice(templates)
            else:
                description = f"Стандартная задача типа {task_type}"
                difficulty = random.randint(1, 5)

        # Валидация сложности
        if difficulty is None:
            difficulty = random.randint(1, 5)

        if not 1 <= difficulty <= 5:
            raise ValueError("Сложность должна быть от 1 до 5")

        return task_class(description, difficulty)

    @classmethod
    def get_available_types(cls):
        """Получение списка доступных типов задач"""
        return list(cls._task_types.keys())

    @classmethod
    def add_custom_task(cls, task_type, description, difficulty):
        """Добавление пользовательской задачи"""
        if task_type not in cls._task_types:
            raise ValueError(f"Неизвестный тип задачи: {task_type}")

        # Добавляем в шаблоны для возможности генерации в будущем
        if task_type not in cls._task_templates:
            cls._task_templates[task_type] = []

        cls._task_templates[task_type].append((description, difficulty))
        return cls.create_task(task_type, description, difficulty)


# ------------------ Генератор задач ------------------
class RandomTaskGenerator:
    """Основной класс приложения"""

    def __init__(self):
        self.history = deque(maxlen=100)  # очередь из 100 последних задач
        self.data_file = "task_history.json"
        self.factory = TaskFactory()
        self.load_history()

    def generate_random_task(self, task_type=None, difficulty=None):
        """Генерация случайной задачи"""
        available_types = self.factory.get_available_types()

        # Если тип не указан, выбираем случайный
        if task_type is None:
            task_type = random.choice(available_types)

        # Если сложность указана, ищем задачу подходящей сложности
        task = None
        if difficulty is not None:
            # Пытаемся найти задачу нужной сложности
            for _ in range(50):  # ограничиваем попытки
                task = self.factory.create_task(task_type)
                if task.difficulty == difficulty:
                    break
                task = None

        if task is None:
            task = self.factory.create_task(task_type, difficulty=difficulty)

        # Добавляем в историю
        self.history.append(task)
        self.save_history()
        return task

    def get_filtered_tasks(self, task_type=None, difficulty=None):
        """Получение отфильтрованных задач из истории"""
        filtered = list(self.history)

        if task_type and task_type != "Все":
            filtered = [t for t in filtered if t.type == task_type]

        if difficulty is not None:
            filtered = [t for t in filtered if t.difficulty == difficulty]

        return filtered

    def add_custom_task(self, task_type, description, difficulty):
        """Добавление пользовательской задачи"""
        # Валидация
        if not description or not description.strip():
            raise ValueError("Описание задачи не может быть пустым")

        if not 1 <= difficulty <= 5:
            raise ValueError("Сложность должна быть от 1 до 5")

        if task_type not in self.factory.get_available_types():
            raise ValueError(f"Неизвестный тип задачи: {task_type}")

        task = self.factory.add_custom_task(task_type, description.strip(), difficulty)
        self.history.append(task)
        self.save_history()
        return task

    def clear_history(self):
        """Очистка истории"""
        self.history.clear()
        self.save_history()

    def save_history(self):
        """Сохранение истории в JSON"""
        data = {
            'history': [task.to_dict() for task in self.history],
            'templates': self.factory._task_templates
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    # Загрузка истории
                    self.history.clear()
                    for task_data in data.get('history', []):
                        task = Task.from_dict(task_data)
                        self.history.append(task)

                    # Загрузка шаблонов
                    templates = data.get('templates', {})
                    for task_type, tasks in templates.items():
                        if task_type in self.factory._task_templates:
                            self.factory._task_templates[task_type] = tasks
            except:
                pass

    def get_stats(self):
        """Получение статистики по истории"""
        if not self.history:
            return "История пуста"

        total = len(self.history)
        by_type = {}
        by_difficulty = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

        for task in self.history:
            by_type[task.type] = by_type.get(task.type, 0) + 1
            by_difficulty[task.difficulty] += 1

        stats = f"\n📊 Статистика ({total} задач):\n"
        stats += "По типам:\n"
        for t, count in sorted(by_type.items()):
            stats += f"  {t}: {count} ({count/total*100:.1f}%)\n"

        stats += "По сложности:\n"
        diff_names = {1: "★", 2: "★★", 3: "★★★", 4: "★★★★", 5: "★★★★★"}
        for d, count in sorted(by_difficulty.items()):
            stats += f"  {diff_names[d]}: {count} ({count/total*100:.1f}%)\n"

        return stats


# ------------------ Консольный интерфейс ------------------
def print_header():
    """Печать заголовка"""
    print("\n" + "="*60)
    print("      🎲 RANDOM TASK GENERATOR 🎲")
    print("="*60)


def print_menu():
    """Печать меню"""
    print("\n📋 МЕНЮ:")
    print("  1. 🎯 Сгенерировать случайную задачу")
    print("  2. 📋 Показать историю задач")
    print("  3. 🔍 Фильтровать задачи")
    print("  4. ➕ Добавить свою задачу")
    print("  5. 📊 Показать статистику")
    print("  6. 🗑️ Очистить историю")
    print("  7. 💾 Сохранить историю в JSON")
    print("  8. 📂 Загрузить историю из JSON")
    print("  0. 🚪 Выход")


def show_history(generator, task_type=None, difficulty=None):
    """Показать историю (с фильтрацией)"""
    tasks = generator.get_filtered_tasks(task_type, difficulty)

    if not tasks:
        print("\n❌ Задачи не найдены!")
        return

    print(f"\n📝 История ({len(tasks)} задач):")
    print("-"*60)
    for i, task in enumerate(tasks, 1):
        print(f"{i:3}. {task}")


def filter_menu(generator):
    """Меню фильтрации"""
    print("\n🔍 ФИЛЬТРАЦИЯ ЗАДАЧ:")
    print("  1. По типу")
    print("  2. По сложности")
    print("  3. По типу и сложности")

    choice = input("\nВыберите опцию (1-3): ").strip()

    task_type = None
    difficulty = None

    if choice in ['1', '3']:
        types = generator.factory.get_available_types()
        print("\nДоступные типы:")
        for i, t in enumerate(types, 1):
            print(f"  {i}. {t}")
        print(f"  {len(types)+1}. Все")

        try:
            type_choice = int(input("\nВыберите тип: "))
            if 1 <= type_choice <= len(types):
                task_type = types[type_choice - 1]
            elif type_choice == len(types) + 1:
                task_type = "Все"
        except:
            pass

    if choice in ['2', '3']:
        print("\nСложность (1-5, где 1 - легкая, 5 - сложная):")
        print("  1 - ★☆☆☆☆ (очень легко)")
        print("  2 - ★★☆☆☆ (легко)")
        print("  3 - ★★★☆☆ (средне)")
        print("  4 - ★★★★☆ (сложно)")
        print("  5 - ★★★★★ (очень сложно)")

        try:
            diff = int(input("\nВведите сложность (1-5): "))
            if 1 <= diff <= 5:
                difficulty = diff
        except:
            pass

    show_history(generator, task_type, difficulty)


def add_custom_task(generator):
    """Добавление пользовательской задачи"""
    print("\n➕ ДОБАВЛЕНИЕ СВОЕЙ ЗАДАЧИ:")

    # Выбор типа
    types = generator.factory.get_available_types()
    print("\nДоступные типы:")
    for i, t in enumerate(types, 1):
        print(f"  {i}. {t}")

    try:
        type_choice = int(input("\nВыберите тип (1-{}): ".format(len(types))))
        if not 1 <= type_choice <= len(types):
            print("❌ Неверный выбор типа!")
            return
        task_type = types[type_choice - 1]
    except:
        print("❌ Неверный ввод!")
        return

    # Ввод описания
    description = input("Введите описание задачи: ").strip()
    if not description:
        print("❌ Описание не может быть пустым!")
        return

    # Ввод сложности
    try:
        difficulty = int(input("Введите сложность (1-5): "))
        if not 1 <= difficulty <= 5:
            print("❌ Сложность должна быть от 1 до 5!")
            return
    except:
        print("❌ Неверный ввод сложности!")
        return

    try:
        task = generator.add_custom_task(task_type, description, difficulty)
        print(f"\n✅ Задача успешно добавлена!")
        print(f"   {task}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def main():
    """Главная функция"""
    generator = RandomTaskGenerator()

    while True:
        print_header()
        print_menu()

        choice = input("\n👉 Ваш выбор: ").strip()

        if choice == '1':
            # Генерация задачи
            print("\n🎲 ГЕНЕРАЦИЯ ЗАДАЧИ:")

            # Опциональный выбор типа
            types = generator.factory.get_available_types()
            print("\nВыберите тип (Enter - случайный):")
            for i, t in enumerate(types, 1):
                print(f"  {i}. {t}")
            print("  0. Случайный тип")

            type_choice = input("\nВаш выбор: ").strip()
            task_type = None
            if type_choice and type_choice.isdigit():
                idx = int(type_choice)
                if 1 <= idx <= len(types):
                    task_type = types[idx - 1]

            # Опциональный выбор сложности
            print("\nСложность (Enter - любая, 1-5):")
            diff_choice = input("Ваш выбор: ").strip()
            difficulty = None
            if diff_choice and diff_choice.isdigit():
                diff = int(diff_choice)
                if 1 <= diff <= 5:
                    difficulty = diff

            task = generator.generate_random_task(task_type, difficulty)
            print(f"\n✨ ВАША ЗАДАЧА НА СЕГОДНЯ ✨")
            print(f"   {task}")
            input("\nНажмите Enter для продолжения...")

        elif choice == '2':
            show_history(generator)
            input("\nНажмите Enter для продолжения...")

        elif choice == '3':
            filter_menu(generator)
            input("\nНажмите Enter для продолжения...")

        elif choice == '4':
            add_custom_task(generator)
            input("\nНажмите Enter для продолжения...")

        elif choice == '5':
            print(generator.get_stats())
            input("\nНажмите Enter для продолжения...")

        elif choice == '6':
            confirm = input("\n⚠️ Вы уверены, что хотите очистить всю историю? (y/n): ")
            if confirm.lower() == 'y':
                generator.clear_history()
                print("✅ История очищена!")
            input("\nНажмите Enter для продолжения...")

        elif choice == '7':
            generator.save_history()
            print("✅ История сохранена в JSON!")
            input("\nНажмите Enter для продолжения...")

        elif choice == '8':
            generator.load_history()
            print("✅ История загружена из JSON!")
            input("\nНажмите Enter для продолжения...")

        elif choice == '0':
            print("\n👋 До свидания! Не забывайте выполнять задачи!")
            break

        else:
            print("\n❌ Неверный выбор! Попробуйте снова.")
            input("\nНажмите Enter для продолжения...")


# ------------------ Запуск приложения ------------------
if __name__ == "__main__":
    main()
