# Техническое решение для Form Processor (Часть 3: Процессор форм и примеры)

## Процессор форм

Основной класс, с которым взаимодействует пользователь - это `FormProcessor`. Он обеспечивает управление сессиями, обработку сообщений и выбор инструментов.

```python
# core/form_processor.py
import uuid
from typing import Type, Dict, Any, Optional, List, Union, Tuple
from pydantic import BaseModel, create_model

from ..models.state import FormState, Settings
from ..models.results import FormResult
from ..tools.form_tools import FormTools
from ..tools.analytics_base import BaseAnalyticsTools
from ..core.session_manager import SessionManager
from ..core.orchestrator import Orchestrator
from ..utils.schema_utils import schema_to_model

class FormProcessor:
    """
    Основной класс для работы с формами.
    Обеспечивает:
    - Управление сессиями и состояниями
    - Обработку сообщений пользователя
    - Генерацию ответов и вопросов
    - Интеграцию с внешними системами через JSON-схемы
    """

    def __init__(
        self,
        form_class: Union[Type[BaseModel], Dict[str, Any]],
        analytics_tools: Optional[BaseAnalyticsTools] = None,
        model: str = "openai/gpt-4o-mini",
        openrouter_api_key: Optional[str] = None,
        db_path: str = "sessions.db",
        client_id: str = "default",
        verbose: bool = False
    ):
        """
        Инициализирует процессор форм.

        Args:
            form_class: Класс формы или JSON-схема формы
            analytics_tools: Инструменты для аналитики
            model: Имя модели для использования
            openrouter_api_key: API-ключ для OpenRouter
            db_path: Путь к базе данных
            client_id: ID клиента
            verbose: Подробное логирование
        """
        self.verbose = verbose

        # Обрабатываем случай, когда передана JSON-схема вместо класса
        if isinstance(form_class, dict):
            if self.verbose:
                print("Converting JSON schema to Pydantic model")
            # Преобразуем JSON-схему в класс Pydantic
            self.form_class = schema_to_model(form_class)
            self.form_name = self.form_class.__name__
        else:
            self.form_class = form_class
            self.form_name = form_class.__name__

        self.api_key = openrouter_api_key
        self.client_id = client_id

        # Создаем инструменты для форм
        self.form_tools = FormTools(
            model=model,
            api_key=openrouter_api_key
        )

        # Инициализируем менеджер сессий
        self.session_manager = SessionManager(
            db_path=db_path,
            verbose=verbose
        )

        # Инициализируем оркестратор
        self.orchestrator = Orchestrator(
            form_tools=self.form_tools,
            analytics_tools=analytics_tools,
            model=model,
            api_key=openrouter_api_key
        )

        # Проверяем наличие вложенных моделей
        self._has_nested_models = self._check_for_nested_models(self.form_class)
        if self._has_nested_models and verbose:
            print(f"Form {self.form_name} contains nested models. Special handling will be applied.")

    def _check_for_nested_models(self, model_class: Type[BaseModel]) -> bool:
        """
        Проверяет, содержит ли модель вложенные Pydantic модели.

        Args:
            model_class: Класс модели для проверки

        Returns:
            True, если модель содержит вложенные модели
        """
        schema = model_class.model_json_schema()
        properties = schema.get("properties", {})

        for field_name, field_schema in properties.items():
            field_type = field_schema.get("type")
            if field_type == "object" and "properties" in field_schema:
                return True
            if field_name in model_class.__annotations__:
                field_type = model_class.__annotations__[field_name]
                origin = getattr(field_type, "__origin__", None)
                if origin is None and isinstance(field_type, type) and issubclass(field_type, BaseModel):
                    return True

        return False

    async def initialize(
        self,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        initial_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, str]:
        """
        Инициализирует новую сессию или восстанавливает существующую.

        Args:
            user_id: ID пользователя (если None, будет сгенерирован)
            session_id: ID сессии для восстановления (опционально)
            initial_data: Начальные данные формы (опционально)

        Returns:
            Tuple[str, str]: ID сессии и начальный/текущий вопрос
        """
        # Генерируем ID пользователя, если не предоставлен
        if user_id is None:
            user_id = str(uuid.uuid4())

        # Создаем или восстанавливаем сессию
        if session_id:
            # Восстанавливаем существующую сессию
            self.session_manager.session_id = session_id
            state_dict = await self.session_manager.get_latest_state(session_id)

            if not state_dict:
                raise ValueError(f"Сессия с ID {session_id} не найдена или не содержит состояния")

            # Извлекаем настройки и вопрос
            settings = state_dict.get("settings", {})
            next_question = settings.get("next_question", "Продолжим заполнение формы?")

        else:
            # Создаем новую сессию
            form_data = initial_data or {}
            client_id = self.form_class.__name__.lower()

            # Создаем сессию в менеджере
            session_id = await self.session_manager.create_session(
                user_id=user_id,
                client_id=client_id,
                form_class=self.form_class.__name__
            )

            # Настраиваем начальный вопрос в зависимости от языка
            next_question = "Расскажите о себе, чтобы мы могли заполнить форму."

            # Создаем экземпляр формы с начальными данными
            form_instance = self.form_class(**form_data)

            # Создаем и сохраняем начальное состояние
            initial_state = FormState(
                form=form_instance,
                settings=Settings(next_question=next_question)
            )

            # Сохраняем состояние
            await self.session_manager.save_state(initial_state.model_dump())

        return session_id, next_question

    async def process_message(
        self,
        message: str,
        session_id: str
    ) -> FormResult:
        """
        Обрабатывает сообщение пользователя.

        Args:
            message: Сообщение пользователя
            session_id: ID сессии

        Returns:
            FormResult: Результат обработки сообщения
        """
        # Проверяем, что сессия существует
        if not session_id:
            raise ValueError("ID сессии не указан")

        # Устанавливаем сессию в менеджере
        self.session_manager.session_id = session_id

        # Получаем последнее состояние
        state_dict = await self.session_manager.get_latest_state(session_id)
        if not state_dict:
            raise ValueError(f"Состояние для сессии {session_id} не найдено")

        # Создаем экземпляр формы из данных
        form_data = state_dict.get("form", {})
        form_instance = self.form_class(**form_data)

        # Создаем объект состояния
        settings_data = state_dict.get("settings", {})
        settings = Settings(**settings_data)
        form_state = FormState(form=form_instance, settings=settings)

        # Получаем историю сообщений
        message_history = await self.session_manager.get_messages()

        # Сохраняем сообщение пользователя в истории
        await self.session_manager.save_message("user", message)

        # Получаем информацию о сессии
        session = await self.session_manager.get_session(session_id)
        user_id = session.get("user_id", "")

        # Обрабатываем сообщение через оркестратор
        result = await self.orchestrator.process(
            message=message,
            form_state=form_state,
            form_class=self.form_class,
            session_id=session_id,
            user_id=user_id,
            message_history=message_history
        )

        # Сохраняем ответ ассистента в истории
        await self.session_manager.save_message("assistant", result.message)

        # Обновляем и сохраняем состояние
        updated_form = self.form_class(**result.form_update)
        updated_state = FormState(
            form=updated_form,
            settings=Settings(
                progress=result.progress,
                prev_question=settings.next_question,
                prev_answer=message,
                next_question=result.next_question,
                language=result.user_language
            )
        )

        # Сохраняем обновленное состояние
        await self.session_manager.save_state(updated_state.model_dump())

        return result

## Интеграция с Django

Важный компонент системы - интеграция с Django для работы с хранимыми в базе данных моделями:

```python
# Пример интеграции с Django
from django.db import models
from utils.schema_utils import schema_to_model
import json

# Модель Django для хранения схем форм
class FormSchema(models.Model):
    form_name = models.CharField(max_length=100, unique=True)
    schema = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.form_name

# Функция для извлечения схемы формы из БД и создания процессора
async def get_form_processor(form_name, api_key=None):
    """
    Создает FormProcessor из схемы формы, хранящейся в базе данных.

    Args:
        form_name: Имя формы в базе данных
        api_key: API-ключ для OpenRouter

    Returns:
        Экземпляр FormProcessor с загруженной формой
    """
    try:
        # Получаем схему из базы данных
        form_schema = FormSchema.objects.get(form_name=form_name)
        schema = form_schema.schema

        # Создаем процессор с загруженной схемой
        from pydantic2.agents14.core.form_processor import FormProcessor
        from pydantic2.agents14.examples.startup_form.analytics import StartupAnalytics

        # Создаем аналитические инструменты, если это форма стартапа
        analytics = None
        if form_name.startswith('startup'):
            analytics = StartupAnalytics(api_key=api_key)

        # Инициализируем процессор с формой из схемы
        processor = FormProcessor(
            form_class=schema,  # Передаем схему напрямую
            analytics_tools=analytics,
            openrouter_api_key=api_key,
            verbose=True
        )

        return processor
    except FormSchema.DoesNotExist:
        raise ValueError(f"Form {form_name} not found in database")
    except Exception as e:
        raise Exception(f"Error creating form processor: {e}")
```

Этот подход обеспечивает полную гибкость работы с формами:
1. Схемы форм могут храниться в базе данных и модифицироваться без изменения кода
2. Новые формы могут быть добавлены без перезапуска приложения
3. Унификация представления данных обеспечивает безопасную передачу между системами

## Сохранение данных форм в Django

После заполнения формы, данные могут быть сохранены в соответствующие Django модели:

```python
# Сохранение данных заполненной формы
async def save_form_data(session_id, api_key=None):
    """
    Сохраняет данные заполненной формы из сессии в Django модели.

    Args:
        session_id: ID сессии с заполненной формой
        api_key: API-ключ для OpenRouter

    Returns:
        ID созданной записи с данными
    """
    from pydantic2.agents14.core.session_manager import SessionManager

    # Инициализируем менеджер сессий
    session_manager = SessionManager(verbose=True)
    session_manager.session_id = session_id

    # Получаем информацию о сессии
    session_info = await session_manager.get_session()
    form_name = session_info.get("form_class")

    # Получаем последнее состояние формы
    state_data = await session_manager.get_latest_state()
    if not state_data or "form" not in state_data:
        raise ValueError(f"No form data found for session {session_id}")

    form_data = state_data["form"]
    progress = state_data.get("settings", {}).get("progress", 0)

    # Проверяем, что форма заполнена
    if progress < 100:
        raise ValueError(f"Form is not complete (progress: {progress}%)")

    # Находим соответствующую модель Django и сохраняем данные
    if form_name == "StartupForm":
        from myapp.models import Startup, StartupCompetitor

        # Создаем запись о стартапе
        startup = Startup(
            product=form_data.get("product", ""),
            target_users=form_data.get("target_users", ""),
            business_model=form_data.get("business_model", "")
        )
        startup.save()

        # Сохраняем конкурентов
        competitors = form_data.get("unique_features", [])
        for comp in competitors:
            StartupCompetitor(startup=startup, name=comp).save()

        return startup.id
    else:
        # Сохраняем данные для других типов форм...
        pass
```

## Пример использования

Пример использования процессора форм с вложенной моделью:

```python
from pydantic import BaseModel, Field
from typing import List
import asyncio

# Определение моделей
class StartupData(BaseModel):
    """
    Данные для формы стартапа
    """
    company_name: str = Field(default="", description="Название компании")
    competitors: List[str] = Field(default=[], description="Список конкурентов")
    revenue_model: str = Field(default="", description="Модель монетизации")
    traction: str = Field(default="", description="Текущая тракция")
    funding_rounds: int = Field(default=0, description="Количество раундов финансирования")

class StartupFormSrc(BaseModel):
    """Структура для хранения данных формы стартапа"""
    idea_desc: str = Field(default="", description="Описание идеи стартапа")
    target_mkt: str = Field(default="", description="Информация о целевом рынке")
    biz_model: str = Field(default="", description="Информация о бизнес-модели")
    team_info: str = Field(default="", description="Информация о команде")
    startup_data: StartupData = Field(default=StartupData(), description="Данные стартапа")

# Конвертация в JSON-схему для безопасной передачи
startup_form_schema = StartupFormSrc.model_json_schema()

# Создание модели из JSON-схемы (имитация получения из Django)
from pydantic2.agents14.utils.schema_utils import schema_to_model
StartupForm = schema_to_model(startup_form_schema)

# Создание аналитического инструмента
from pydantic2.agents14.examples.startup_form.analytics import StartupAnalytics
analytics = StartupAnalytics(model="openai/gpt-4o-mini", api_key="your-api-key")

# Инициализация процессора форм
from pydantic2.agents14.core.form_processor import FormProcessor
processor = FormProcessor(
    form_class=StartupForm,  # Модель, созданная из JSON-схемы
    analytics_tools=analytics,
    openrouter_api_key="your-api-key",
    verbose=True
)

async def simulate_dialog():
    # Создание сессии
    session_id, initial_question = await processor.initialize(user_id="user123")
    print(f"Начальный вопрос: {initial_question}")

    # Симуляция диалога
    messages = [
        "Я разрабатываю приложение для автоматизации маркетинга для малого бизнеса",
        "Целевой рынок - предприниматели и малые компании с ограниченным бюджетом на маркетинг",
        "Наша бизнес-модель основана на ежемесячной подписке с разными тарифами",
        "Моя компания называется MarketBoost, у нас уже есть MVP и 50 бета-тестеров",
        "Конкуренты: Mailchimp, HubSpot и несколько небольших локальных компаний",
        "Мы провели один раунд посевного финансирования"
    ]

    for message in messages:
        print(f"\nПользователь: {message}")
        result = await processor.process_message(message, session_id)
        print(f"Ассистент: {result.message}")
        print(f"Прогресс: {result.progress}%")

    # Запрос на анализ
    print("\nПользователь: Проанализируй мой стартап и дай рекомендации")
    result = await processor.process_message("Проанализируй мой стартап и дай рекомендации", session_id)
    print(f"Ассистент: {result.message}")

    # Получаем и выводим историю сессии
    state_history = await processor.session_manager.get_state_history(session_id)
    print(f"\nИстория состояний (количество: {len(state_history)})")

    # Выводим итоговую форму
    final_state = state_history[-1]
    print("\nИтоговые данные формы:")
    print(final_state["form"])

# Запуск симуляции
asyncio.run(simulate_dialog())
```

## Заключение

Система реализует пошаговый чат-движок для форм на базе сессий, что обеспечивает гибкость при прерванных диалогах и отсутствие необходимости в постоянном соединении. При этом полностью используется мощь LLM для интеллектуальной обработки форм, делегируя ключевые решения в модель:

1. **Работа с сессиями вместо прямых соединений** - диалог можно продолжить в любой момент, передав session_id
2. **LLM определяет прогресс** - вместо жестких правил, модель решает когда форма считается заполненной
3. **LLM определяет язык пользователя** - адаптация под язык без явного указания
4. **LLM генерирует релевантные вопросы** - учитывая контекст и историю общения
5. **LLM выполняет аналитику** - когда форма заполнена и пользователь запрашивает анализ

При этом четкое разграничение ответственности между инструментами форм (прогресс < 100%) и аналитическими инструментами (прогресс = 100%) делает систему гибкой и расширяемой.

Особенно важно, что система спроектирована для работы с различными источниками данных, включая Django ORM, благодаря механизму конвертации между моделями и JSON-схемами. Это делает решение универсальным и применимым для широкого спектра задач.
