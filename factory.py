from models import Task, TaskType, Difficulty
import random

class TaskFactory:
    """Абстрактная фабрика для создания задач"""

    # Предопределённые списки задач
    WORK_TASKS = [
        "Написать отчёт", "Провести встречу", "Сделать презентацию",
        "Проверить почту", "Запланировать спринт", "Оптимизировать код"
    ]

    SPORT_TASKS = [
        "Пробежка 5 км", "Йога 30 мин", "Отжимания 50 раз",
        "Плавание в бассейне", "Велосипедная прогулка", "Растяжка"
    ]

    STUDY_TASKS = [
        "Изучить Python", "Почитать книгу", "Посмотреть лекцию",
        "Решить задачи", "Написать конспект", "Пройти онлайн-курс"
    ]

    OTHER_TASKS = [
        "Позвонить другу", "Сходить в магазин", "Убраться в комнате",
        "Приготовить ужин", "Помыть посуду", "Полить цветы"
    ]

    @staticmethod
    def create_work_task(description=None, difficulty=None):
        if description is None:
            description = random.choice(TaskFactory.WORK_TASKS)
        if difficulty is None:
            difficulty = random.choice(list(Difficulty))
        return Task(description, TaskType.WORK, difficulty)

    @staticmethod
    def create_sport_task(description=None, difficulty=None):
        if description is None:
            description = random.choice(TaskFactory.SPORT_TASKS)
        if difficulty is None:
            difficulty = random.choice(list(Difficulty))
        return Task(description, TaskType.SPORT, difficulty)

    @staticmethod
    def create_study_task(description=None, difficulty=None):
        if description is None:
            description = random.choice(TaskFactory.STUDY_TASKS)
        if difficulty is None:
            difficulty = random.choice(list(Difficulty))
        return Task(description, TaskType.STUDY, difficulty)

    @staticmethod
    def create_other_task(description=None, difficulty=None):
        if description is None:
            description = random.choice(TaskFactory.OTHER_TASKS)
        if difficulty is None:
            difficulty = random.choice(list(Difficulty))
        return Task(description, TaskType.OTHER, difficulty)

    @staticmethod
    def create_random_task():
        """Создаёт задачу случайного типа"""
        task_types = [
            TaskFactory.create_work_task,
            TaskFactory.create_sport_task,
            TaskFactory.create_study_task,
            TaskFactory.create_other_task
        ]
        creator = random.choice(task_types)
        return creator()

    @staticmethod
    def create_custom_task(description, type_str, difficulty_str):
        """Создаёт пользовательскую задачу с валидацией"""
        try:
            task_type = TaskType(type_str)
            difficulty = Difficulty(difficulty_str)

            if not description or len(description.strip()) == 0:
                raise ValueError("Описание не может быть пустым")
            if len(description) > 200:
                raise ValueError("Описание не должно превышать 200 символов")

            return Task(description.strip(), task_type, difficulty)
        except ValueError as e:
            raise ValueError(f"Ошибка создания задачи: {e}")
