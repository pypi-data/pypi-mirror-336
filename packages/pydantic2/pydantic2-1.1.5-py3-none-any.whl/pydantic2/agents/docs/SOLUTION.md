# Техническое решение для Form Processor (Часть 1: Ядро и модели)

## Обзор архитектуры

Решение построено на концепции пошагового чат-движка для интеллектуального заполнения форм, использующего сессии вместо прямых WebSocket соединений. Это позволяет создавать долгосрочные диалоги, которые могут быть прерваны и продолжены в любой момент.

Основные принципы решения:

1. **LLM в центре решения**:
   - Расчет прогресса формы выполняется LLM
   - Генерация вопросов основана на контексте и данных пользователя
   - Определение языка пользователя для ответов
   - Интеллектуальное извлечение данных из свободного текста

2. **Два четких вида инструментов**:
   - `FormTools` - для заполнения форм (используется пока прогресс < 100%)
   - `AnalyticsTools` - для анализа данных (используется когда прогресс = 100%)

3. **Сессионный подход**:
   - Каждый диалог сохраняется в базе данных как сессия
   - Состояние формы персистентно и может быть восстановлено по ID
   - Не требуется поддерживать постоянное соединение с клиентом

4. **Интеграция с OpenRouter**:
   - Каждый инструмент использует свою модель через OpenRouter
   - Гибкая настройка параметров для разных задач

5. **Поддержка сложных и вложенных моделей**:
   - Работа с моделями, содержащими вложенные Pydantic структуры
   - Полная поддержка преобразования моделей в JSON-схемы и обратно
   - Специальная обработка для вложенных полей при обновлении данных формы

## Модели данных

### Зависимости инструментов

```python
from typing import Dict, Any, Type, List
from pydantic import BaseModel

class FormDependencies(BaseModel):
    """
    Зависимости для инструментов форм.
    Содержит необходимую информацию для работы инструментов.
    """
    form_class: Type[BaseModel]
    form_data: Dict[str, Any]
    user_id: str
    session_id: str
    progress: int = 0
    message_history: List[Dict[str, Any]] = []
    user_language: str = "ru"
```

### Результат обработки формы

```python
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class FormResult(BaseModel):
    """
    Результат обработки формы.
    Содержит обновленные данные формы, прогресс и следующий вопрос.
    """
    message: str
    form_update: Dict[str, Any]
    progress: int
    next_question: str
    user_language: str = "ru"
    insights: Optional[List[str]] = None
```

### Состояние формы

```python
from typing import Dict, Any
from pydantic import BaseModel

class Settings(BaseModel):
    """
    Настройки формы.
    Содержит информацию о текущем состоянии заполнения.
    """
    progress: int = 0
    next_question: str = ""
    prev_question: str = ""
    prev_answer: str = ""
    language: str = "ru"

class FormState(BaseModel):
    """
    Состояние формы.
    Включает данные формы и настройки.
    """
    form: Dict[str, Any]
    settings: Settings
```

## Работа с вложенными моделями

Система полностью поддерживает сложные формы с вложенными Pydantic моделями:

```python
from pydantic import BaseModel, Field
from typing import List

class StartupData(BaseModel):
    """Вложенная модель с данными стартапа"""
    company_name: str = Field(default="", description="Название компании")
    competitors: List[str] = Field(default=[], description="Список конкурентов")
    revenue_model: str = Field(default="", description="Модель монетизации")

class StartupFormSrc(BaseModel):
    """Основная модель формы стартапа"""
    idea_desc: str = Field(default="", description="Описание идеи")
    target_mkt: str = Field(default="", description="Целевой рынок")
    startup_data: StartupData = Field(default=StartupData(), description="Данные стартапа")
```

При обработке вложенных моделей система использует специальную логику обновления данных, которая рекурсивно обрабатывает вложенные объекты, сохраняя интеграцию полей и правильно объединяя списки.

## Интеграция с Django и другими системами

Важным аспектом системы является возможность безопасной работы с внешними источниками данных (например, Django моделями). Для этого реализовано преобразование моделей в JSON-схемы и обратно:

```python
# Преобразуем модель в JSON-схему для хранения в БД или передачи
startup_form_schema = StartupFormSrc.model_json_schema()

# Восстанавливаем модель из схемы
from utils.schema_utils import schema_to_model
StartupForm = schema_to_model(startup_form_schema)

# Используем воссозданную модель
processor = FormProcessor(form_class=StartupForm)
```

Это важная мера предосторожности, гарантирующая целостность данных и корректность типов при работе с моделями из разных источников.

## Менеджер сессий

Менеджер сессий отвечает за сохранение и восстановление состояния формы, а также за историю сообщений. Он взаимодействует с базой данных через ORM Peewee.

```python
import uuid
import json
import datetime
from typing import Dict, Any, List, Optional
import peewee as pw
from pathlib import Path

class SessionManager:
    """
    Менеджер сессий для работы с состоянием и историей сообщений.
    Обеспечивает персистентность через Peewee ORM.
    """

    def __init__(self, db_path: str = "sessions.db", verbose: bool = False):
        """
        Инициализирует менеджер сессий.

        Args:
            db_path: Путь к файлу базы данных
            verbose: Подробное логирование
        """
        self.db_path = db_path
        self.verbose = verbose
        self.session_id = None
        self._setup_database()

    # ... (остальные методы из исходного кода)

    async def get_state_history(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Получает историю состояний формы.

        Args:
            session_id: ID сессии (если None, используется текущая сессия)

        Returns:
            Список словарей с данными состояний, отсортированных по времени создания
        """
        sid = session_id or self.session_id
        if not sid:
            return []

        try:
            session = Session.get(Session.session_id == sid)
            states = (State
                     .select()
                     .where(State.session == session)
                     .order_by(State.created_at))

            return [
                {**json.loads(state.data), "created_at": state.created_at.isoformat()}
                for state in states
            ]
        except Exception as e:
            if self.verbose:
                print(f"Error retrieving state history: {e}")
            return []

    async def check_database(self) -> bool:
        """
        Проверяет доступность базы данных.

        Returns:
            True если база данных доступна, иначе False
        """
        try:
            # Check if database is available
            if db.is_closed():
                db.connect()

            # Try executing a simple query
            Session.select().limit(1).exists()
            return True
        except Exception as e:
            if self.verbose:
                print(f"Database check failed: {e}")
            return False

    async def debug_session_info(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Собирает подробную отладочную информацию о сессии.

        Args:
            session_id: ID сессии (если None, используется текущая сессия)

        Returns:
            Словарь с отладочной информацией
        """
        sid = session_id or self.session_id
        if not sid:
            return {"error": "No session ID provided"}

        try:
            session = Session.get(Session.session_id == sid)

            # Get statistics about the session
            state_count = State.select().where(State.session == session).count()
            message_count = Message.select().where(Message.session == session).count()

            # Calculate session age
            session_age = (datetime.datetime.now() - session.created_at).total_seconds()

            # Get latest state progress
            latest_state = (State
                           .select()
                           .where(State.session == session)
                           .order_by(State.created_at.desc())
                           .first())

            progress = 0
            if latest_state:
                state_data = json.loads(latest_state.data)
                settings = state_data.get("settings", {})
                progress = settings.get("progress", 0)

            return {
                "session_id": sid,
                "user_id": session.user_id,
                "client_id": session.client_id,
                "form_class": session.form_class,
                "created_at": session.created_at.isoformat(),
                "age": session_age,
                "state_count": state_count,
                "message_count": message_count,
                "current_progress": progress
            }
        except Session.DoesNotExist:
            return {"error": f"Session {sid} not found"}
        except Exception as e:
            return {"error": str(e)}
```

Такая архитектура позволяет эффективно работать с формами любой сложности, обеспечивая надежное хранение состояний и интеграцию с внешними системами через механизм JSON-схем.
