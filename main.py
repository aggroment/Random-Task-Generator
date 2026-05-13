from models import TaskType, Difficulty
from factory import TaskFactory
from storage import TaskHistory

class RandomTaskGenerator:
    """Главный класс приложения"""

    def __init__(self):
        self.history = TaskHistory()

    def display_menu(self):
        print("\n" + "="*50)
        print("🎲 RANDOM TASK GENERATOR")
        print("="*50)
        print("1. 🎯 Сгенерировать случайную задачу")
        print("2. 📝 Добавить свою задачу")
        print("3. 📋 Показать историю задач")
        print("4. 🔍 Фильтровать по типу")
        print("5. ⭐ Фильтровать по сложности")
        print("6. 🗑️  Очистить историю")
        print("0. 🚪 Выход")
        print("-"*50)

    def generate_random_task(self):
        """Генерация случайной задачи"""
        task = TaskFactory.create_random_task()
        self.history.add_task(task)
        print(f"\n✨ Сгенерирована задача:\n{task}")
        return task

    def add_custom_task(self):
        """Добавление пользовательской задачи"""
        print("\n📝 Добавление новой задачи")

        try:
            description = input("Описание задачи: ").strip()
            if not description:
                print("❌ Ошибка: описание не может быть пустым")
                return

            print("\nДоступные типы:")
            for t in TaskType:
                print(f"  - {t.value}")
            type_str = input("Тип задачи: ").strip()

            print("\nДоступные сложности:")
            for d in Difficulty:
                print(f"  - {d.value}")
            difficulty_str = input("Сложность: ").strip()

            task = TaskFactory.create_custom_task(description, type_str, difficulty_str)
            self.history.add_task(task)
            print(f"\n✅ Задача добавлена:\n{task}")

        except ValueError as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Непредвиденная ошибка: {e}")

    def show_history(self):
        """Показать все задачи из истории"""
        tasks = self.history.get_all_tasks()

        if not tasks:
            print("\n📭 История пуста. Сначала сгенерируйте или добавьте задачи.")
            return

        print(f"\n📋 История задач (всего: {len(tasks)}):")
        print("-"*50)
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

    def filter_by_type(self):
        """Фильтрация по типу"""
        print("\n🔍 Фильтр по типу задачи:")
        for t in TaskType:
            print(f"  - {t.value}")

        type_str = input("Выберите тип: ").strip()

        try:
            task_type = TaskType(type_str)
            filtered = self.history.get_tasks_by_type(task_type)

            if not filtered:
                print(f"\n📭 Нет задач типа '{task_type.value}'")
            else:
                print(f"\n📋 Задачи типа '{task_type.value}' (всего: {len(filtered)}):")
                for i, task in enumerate(filtered, 1):
                    print(f"{i}. {task}")
        except ValueError:
            print("❌ Неверный тип задачи")

    def filter_by_difficulty(self):
        """Фильтрация по сложности"""
        print("\n🔍 Фильтр по сложности:")
        for d in Difficulty:
            print(f"  - {d.value}")

        difficulty_str = input("Выберите сложность: ").strip()

        try:
            difficulty = Difficulty(difficulty_str)
            filtered = self.history.get_tasks_by_difficulty(difficulty)

            if not filtered:
                print(f"\n📭 Нет задач сложности '{difficulty.value}'")
            else:
                print(f"\n📋 Задачи сложности '{difficulty.value}' (всего: {len(filtered)}):")
                for i, task in enumerate(filtered, 1):
                    print(f"{i}. {task}")
        except ValueError:
            print("❌ Неверная сложность")

    def clear_history(self):
        """Очистка истории"""
        confirm = input("\n⚠️  Вы уверены, что хотите очистить всю историю? (y/n): ")
        if confirm.lower() == 'y':
            self.history.clear_history()
            print("✅ История очищена")
        else:
            print("❌ Очистка отменена")

    def run(self):
        """Запуск приложения"""
        print("\n🎲 Добро пожаловать в Random Task Generator!")
        print("Автор: Иван Петров")

        while True:
            self.display_menu()
            choice = input("Выберите действие: ").strip()

            if choice == "1":
                self.generate_random_task()
            elif choice == "2":
                self.add_custom_task()
            elif choice == "3":
                self.show_history()
            elif choice == "4":
                self.filter_by_type()
            elif choice == "5":
                self.filter_by_difficulty()
            elif choice == "6":
                self.clear_history()
            elif choice == "0":
                print("\n👋 До свидания! Спасибо за использование программы!")
                break
            else:
                print("\n❌ Неверный выбор. Пожалуйста, выберите действие из меню.")

            input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    app = RandomTaskGenerator()
    app.run()
