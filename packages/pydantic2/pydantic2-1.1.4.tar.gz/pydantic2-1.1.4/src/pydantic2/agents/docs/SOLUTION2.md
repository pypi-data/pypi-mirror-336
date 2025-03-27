# Техническое решение для Form Processor (Часть 2: Инструменты и оркестрация)

## Инструменты для форм

Система построена на основе пошагового чат-движка с сессионной архитектурой и делегирует всю сложную логику в LLM. Инструменты формы разработаны в соответствии с этой философией, обеспечивая простое взаимодействие между сессиями и LLM.

### Инструменты для работы с формами

```python
# tools/form_tools.py
from typing import Dict, Any, List, Optional, Type
from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from ..models.dependencies import FormDependencies
from pydantic import BaseModel

class FormTools:
    """
    Набор инструментов для работы с формами.
    ВАЖНО: Эти инструменты должны использоваться ТОЛЬКО когда прогресс заполнения формы < 100%.
    Основная задача - извлечение данных из сообщений пользователя и управление прогрессом формы.
    """

    def __init__(self, model: str = "openai/gpt-4o-mini", api_key: str = None):
        """Инициализирует инструменты для форм."""
        self.model_name = model
        self.api_key = api_key
        self.model = self._create_model()
        self.agent = Agent(model=self.model)
        self._register_tools()

    def _create_model(self) -> OpenAIModel:
        """Создает модель для инструментов формы."""
        provider = OpenAIProvider(
            base_url="https://openrouter.ai/api/v1",  # Или другой API
            api_key=self.api_key,
            headers={"HTTP-Referer": "https://aiforma.app"}
        )

        return OpenAIModel(
            self.model_name,
            provider=provider
        )

    def _register_tools(self):
        """Регистрирует инструменты в агенте."""

        @self.agent.tool
        async def get_form_schema(ctx: RunContext[FormDependencies]) -> Dict[str, Any]:
            """
            Получает JSON-схему формы с описаниями полей.
            Используйте этот инструмент, чтобы понять структуру формы.
            """
            form_class = ctx.deps.form_class
            return form_class.model_json_schema()

        @self.agent.tool
        async def extract_data_from_message(
            ctx: RunContext[FormDependencies],
            message: str
        ) -> Dict[str, Any]:
            """
            Извлекает данные из сообщения пользователя и обновляет форму.
            Используйте этот инструмент, когда пользователь предоставляет информацию для заполнения формы.
            """
            current_data = ctx.deps.form_data.copy()
            schema = await get_form_schema(ctx)
            properties = schema.get("properties", {})

            # Проверяем наличие вложенных объектов
            has_nested_objects = False
            nested_objects_info = {}

            for field_name, field_schema in properties.items():
                if field_schema.get("type") == "object" and "properties" in field_schema:
                    has_nested_objects = True
                    nested_objects_info[field_name] = {
                        "description": field_schema.get("description", f"Вложенный объект {field_name}"),
                        "properties": field_schema.get("properties", {})
                    }

            # Промпт для извлечения данных
            system_prompt = f"""
            Вы - инструмент для извлечения данных из текста пользователя.

            ЗАДАЧА:
            1. Проанализируйте сообщение пользователя
            2. Извлеките всю информацию, которая может быть использована для заполнения формы
            3. Верните обновленный словарь данных формы

            ИНСТРУКЦИИ:
            - Сохраняйте существующие значения, если нет явных противоречий
            - Обновляйте только те поля, для которых есть информация в сообщении
            - Для списков, добавляйте новые элементы, а не заменяйте существующие
            - Определите язык пользователя для последующих взаимодействий
            """

            # Если есть вложенные объекты, добавляем информацию о них
            if has_nested_objects:
                system_prompt += f"""

                ВАЖНО: Форма содержит вложенные объекты:
                {json.dumps(nested_objects_info, indent=2, ensure_ascii=False)}

                При обнаружении данных для вложенных объектов, сохраняйте правильную структуру в JSON.
                Например: {{"nested_field": {{"subfield1": "value1", "subfield2": "value2"}}}}
                """

            system_prompt += f"""
            ТЕКУЩИЕ ДАННЫЕ ФОРМЫ:
            {current_data}

            СТРУКТУРА ФОРМЫ:
            {properties}
            """

            # Запрос к модели
            result = await ctx.model.invoke(
                system_prompt,
                message,
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            try:
                updated_data = result.choices[0].message.content
                # Если результат в формате JSON строки
                if isinstance(updated_data, str):
                    import json
                    updated_data = json.loads(updated_data)

                # Обработка специальных случаев (например, списки)
                for key, value in updated_data.items():
                    if key in current_data and isinstance(current_data[key], list) and isinstance(value, list):
                        # Для списков, объединяем значения вместо замены
                        updated_data[key] = list(set(current_data[key] + value))
                    elif key in current_data and isinstance(current_data[key], dict) and isinstance(value, dict):
                        # Для вложенных объектов, рекурсивно обновляем
                        merged_dict = current_data[key].copy()
                        for nested_key, nested_value in value.items():
                            if nested_key in merged_dict and isinstance(merged_dict[nested_key], list) and isinstance(nested_value, list):
                                # Объединяем списки во вложенных объектах
                                merged_dict[nested_key] = list(set(merged_dict[nested_key] + nested_value))
                            else:
                                merged_dict[nested_key] = nested_value
                        updated_data[key] = merged_dict

                return updated_data
            except Exception as e:
                # В случае ошибки возвращаем исходные данные
                if ctx.deps.verbose:
                    print(f"Error extracting data: {e}")
                return current_data

        @self.agent.tool
        async def extract_data_from_yaml(
            ctx: RunContext[FormDependencies],
            message: str
        ) -> Dict[str, Any]:
            """
            Извлекает данные из сообщения пользователя и преобразует их в YAML для более наглядной
            обработки многомерных данных.
            Используйте этот инструмент, когда пользователь предоставляет сложную структурированную информацию
            с вложенными объектами и списками.
            """
            current_data = ctx.deps.form_data.copy()
            schema = await get_form_schema(ctx)
            properties = schema.get("properties", {})

            # Проверяем сложность модели - если есть много вложенных объектов или массивов, используем YAML
            complex_model = False
            nested_structure = {}

            for field_name, field_schema in properties.items():
                if field_schema.get("type") == "object" and "properties" in field_schema:
                    complex_model = True
                    nested_structure[field_name] = {
                        "type": "object",
                        "properties": field_schema.get("properties", {})
                    }
                elif field_schema.get("type") == "array" and field_schema.get("items", {}).get("type") == "object":
                    complex_model = True
                    nested_structure[field_name] = {
                        "type": "array",
                        "items": field_schema.get("items", {})
                    }

            # Промпт для извлечения данных в YAML формате
            system_prompt = f"""
            Вы - инструмент для извлечения структурированных данных из текста пользователя.

            ЗАДАЧА:
            1. Проанализируйте сообщение пользователя
            2. Извлеките всю информацию, которая может быть использована для заполнения формы
            3. Верните обновленный словарь данных формы в формате YAML

            YAML выбран из-за его наглядности при работе с многомерными вложенными структурами данных.

            ИНСТРУКЦИИ:
            - Сохраняйте существующие значения, если нет явных противоречий
            - Обновляйте только те поля, для которых есть информация в сообщении
            - Используйте правильные отступы для вложенных структур
            - Для списков объектов используйте YAML синтаксис с дефисами

            СТРУКТУРА ФОРМЫ:
            {properties}

            ТЕКУЩИЕ ДАННЫЕ ФОРМЫ:
            {yaml.dump(current_data, sort_keys=False, default_flow_style=False)}

            СЛОЖНЫЕ ВЛОЖЕННЫЕ ОБЪЕКТЫ И МАССИВЫ:
            {yaml.dump(nested_structure, sort_keys=False, default_flow_style=False) if complex_model else "Отсутствуют"}

            Верните ТОЛЬКО YAML с обновленными данными, без дополнительных пояснений.
            """

            # Запрос к модели
            result = await ctx.model.invoke(
                system_prompt,
                message,
                temperature=0.1
            )

            try:
                yaml_result = result.choices[0].message.content.strip()
                import yaml
                updated_data = yaml.safe_load(yaml_result)

                if not isinstance(updated_data, dict):
                    # Если результат не словарь, возвращаем исходные данные
                    return current_data

                # Процесс слияния данных аналогичен JSON-версии
                for key, value in updated_data.items():
                    if key in current_data and isinstance(current_data[key], list) and isinstance(value, list):
                        # Объединяем списки
                        updated_data[key] = list(set(current_data[key] + value))
                    elif key in current_data and isinstance(current_data[key], dict) and isinstance(value, dict):
                        # Рекурсивно объединяем вложенные словари
                        merged_dict = current_data[key].copy()
                        for nested_key, nested_value in value.items():
                            if nested_key in merged_dict and isinstance(merged_dict[nested_key], list) and isinstance(nested_value, list):
                                merged_dict[nested_key] = list(set(merged_dict[nested_key] + nested_value))
                            else:
                                merged_dict[nested_key] = nested_value
                        updated_data[key] = merged_dict

                return updated_data

            except Exception as e:
                # В случае ошибки возвращаем исходные данные
                if ctx.deps.verbose:
                    print(f"Error extracting data from YAML: {e}")
                return current_data

        @self.agent.tool
        async def detect_user_language(
            ctx: RunContext[FormDependencies],
            message: str
        ) -> str:
            """
            Определяет язык пользователя из сообщения.
            Используйте этот инструмент, чтобы адаптировать ответы под язык пользователя.
            """
            system_prompt = """
            Определите язык пользователя из сообщения.
            Верните только код языка (например, 'en', 'ru', 'fr').
            """

            result = await ctx.model.invoke(system_prompt, message, temperature=0.1)
            language = result.choices[0].message.content.strip().lower()

            # Проверка на корректность кода языка
            if len(language) > 5:
                # Если ответ не похож на код языка, используем английский по умолчанию
                return "en"

            return language

        @self.agent.tool
        async def calculate_progress(
            ctx: RunContext[FormDependencies],
            form_data: Dict[str, Any]
        ) -> int:
            """
            Рассчитывает прогресс заполнения формы (0-100%).
            Используйте этот инструмент после обновления данных формы, чтобы определить, насколько форма заполнена.
            """
            schema = await get_form_schema(ctx)
            properties = schema.get("properties", {})

            # Проверяем наличие вложенных объектов
            flattened_fields = {}

            for field_name, field_schema in properties.items():
                if field_schema.get("type") == "object" and "properties" in field_schema:
                    # Для вложенных объектов, добавляем его поля с префиксом
                    nested_props = field_schema.get("properties", {})
                    for nested_field, nested_schema in nested_props.items():
                        flattened_fields[f"{field_name}.{nested_field}"] = nested_schema
                else:
                    flattened_fields[field_name] = field_schema

            # Расширяем промпт информацией о вложенных полях
            system_prompt = f"""
            Оцените процент заполнения формы на основе имеющихся данных.

            ЗАДАЧА:
            1. Проанализируйте текущие данные формы
            2. Сравните с требуемыми полями из схемы
            3. Верните число от 0 до 100, представляющее процент заполнения

            ПРАВИЛА РАСЧЕТА:
            - Пустые строки или null-значения считаются незаполненными
            - Пустые списки считаются незаполненными
            - Качество заполнения также имеет значение (подробные ответы = более высокий процент)
            - Для полного заполнения (100%) все обязательные поля должны быть заполнены и содержать качественную информацию
            """

            # Добавляем информацию о вложенных полях
            if len(flattened_fields) > len(properties):
                system_prompt += f"""

                ВАЖНО: Форма содержит вложенные поля. Вот полный список всех полей (включая вложенные):
                {json.dumps(flattened_fields, indent=2, ensure_ascii=False)}

                При расчете прогресса, учитывайте и вложенные поля тоже.
                """

            system_prompt += f"""
            ТЕКУЩИЕ ДАННЫЕ ФОРМЫ:
            {form_data}

            СТРУКТУРА ФОРМЫ:
            {properties}

            Верните ТОЛЬКО число от 0 до 100 без дополнительного текста.
            """

            result = await ctx.model.invoke(system_prompt, "", temperature=0.1)
            progress_text = result.choices[0].message.content.strip()

            try:
                # Извлекаем число из ответа
                import re
                progress_match = re.search(r'\d+', progress_text)
                if progress_match:
                    progress = int(progress_match.group())
                    # Ограничиваем значение от 0 до 100
                    return max(0, min(100, progress))
                else:
                    # Если не удалось извлечь число, используем эвристику
                    return self._calculate_progress_heuristic(form_data, properties)
            except Exception:
                # В случае ошибки используем простую эвристику
                return self._calculate_progress_heuristic(form_data, properties)

        def _calculate_progress_heuristic(self, form_data, properties):
            """Вспомогательный метод для расчета прогресса на основе эвристики."""
            total_fields = 0
            filled_fields = 0

            def count_fields_recursive(data, schema, prefix=""):
                nonlocal total_fields, filled_fields

                for key, value in schema.items():
                    if key.startswith("$") or key in ["definitions", "additionalProperties"]:
                        continue

                    field_path = f"{prefix}.{key}" if prefix else key
                    field_type = value.get("type")

                    if field_type == "object" and "properties" in value:
                        # Для вложенных объектов, рекурсивно обрабатываем
                        nested_data = data.get(key, {}) if isinstance(data, dict) else {}
                        count_fields_recursive(nested_data, value.get("properties", {}), field_path)
                    else:
                        total_fields += 1

                        # Проверяем заполненность поля
                        if isinstance(data, dict) and key in data:
                            field_value = data[key]
                            is_filled = False

                            if isinstance(field_value, str) and field_value.strip():
                                is_filled = True
                            elif isinstance(field_value, list) and field_value:
                                is_filled = True
                            elif isinstance(field_value, dict) and field_value:
                                is_filled = True
                            elif field_value is not None and not isinstance(field_value, (str, list, dict)):
                                is_filled = True

                            if is_filled:
                                filled_fields += 1

            count_fields_recursive(form_data, properties)

            if total_fields == 0:
                return 100

            return min(100, int((filled_fields / total_fields) * 100))

        @self.agent.tool
        async def generate_next_question(
            ctx: RunContext[FormDependencies],
            form_data: Dict[str, Any]
        ) -> str:
            """
            Генерирует следующий вопрос для пользователя.
            Используйте этот инструмент, чтобы определить, какой вопрос задать пользователю дальше.
            """
            progress = await calculate_progress(ctx, form_data)
            schema = await get_form_schema(ctx)
            properties = schema.get("properties", {})
            message_history = ctx.deps.message_history
            user_language = ctx.deps.user_language or "en"

            # Если форма заполнена
            if progress >= 100:
                if user_language == "ru":
                    return "Форма заполнена! Хотите получить анализ данных?"
                else:
                    return "The form is complete! Would you like to analyze the data?"

            # Проверяем наличие вложенных объектов
            has_nested_objects = False
            nested_fields_info = []

            for field_name, field_schema in properties.items():
                if field_schema.get("type") == "object" and "properties" in field_schema:
                    has_nested_objects = True
                    nested_props = field_schema.get("properties", {})
                    for nested_field, nested_schema in nested_props.items():
                        field_path = f"{field_name}.{nested_field}"
                        nested_fields_info.append({
                            "path": field_path,
                            "description": nested_schema.get("description", nested_field),
                            "filled": self._is_field_filled(form_data, field_name, nested_field)
                        })

            system_prompt = f"""
            Сгенерируйте следующий вопрос для пользователя на основе текущего состояния формы.

            ЗАДАЧА:
            1. Проанализируйте, какие поля формы еще не заполнены или заполнены неполно
            2. Выберите наиболее логичный следующий вопрос с учетом уже заполненных полей
            3. Сформулируйте вопрос естественно и конкретно

            ПРАВИЛА:
            - Вопрос должен фокусироваться на незаполненных полях
            - Используйте контекст предыдущих взаимодействий, чтобы не повторяться
            - Вопрос должен быть на языке пользователя (предпочтительно {user_language})
            - Вопрос должен быть конкретным и не слишком общим
            """

            # Если есть вложенные объекты, добавляем информацию о них
            if has_nested_objects:
                system_prompt += f"""

                ВАЖНО: Форма содержит вложенные поля. Вот информация о вложенных полях:
                {json.dumps(nested_fields_info, indent=2, ensure_ascii=False)}

                При составлении вопроса, вы можете спрашивать и о вложенных полях, если они не заполнены.
                """

            system_prompt += f"""
            ТЕКУЩИЕ ДАННЫЕ ФОРМЫ:
            {form_data}

            СТРУКТУРА ФОРМЫ:
            {properties}

            ИСТОРИЯ СООБЩЕНИЙ:
            {message_history[-5:] if len(message_history) > 0 else "История пуста"}

            Верните только текст вопроса без дополнительных пояснений.
            """

            result = await ctx.model.invoke(system_prompt, "", temperature=0.7)
            next_question = result.choices[0].message.content.strip()

            return next_question

        def _is_field_filled(self, form_data, parent_field, nested_field):
            """Проверяет, заполнено ли вложенное поле."""
            if parent_field not in form_data or not isinstance(form_data[parent_field], dict):
                return False

            nested_data = form_data[parent_field]
            if nested_field not in nested_data:
                return False

            value = nested_data[nested_field]

            if isinstance(value, str) and value.strip():
                return True
            elif isinstance(value, list) and value:
                return True
            elif isinstance(value, dict) and value:
                return True
            elif value is not None and not isinstance(value, (str, list, dict)):
                return True

            return False

    async def get_form_schema(self, form_class) -> Dict[str, Any]:
        """Получает JSON-схему формы."""
        # Проверяем, не является ли форма строкой JSON-схемы
        if isinstance(form_class, dict):
            # Это уже JSON-схема
            return form_class
        return form_class.model_json_schema()

    async def extract_data_from_message(
        self, message: str, form_data: Dict[str, Any], form_class
    ) -> Dict[str, Any]:
        """Извлекает данные из сообщения."""
        deps = FormDependencies(
            form_class=form_class,
            form_data=form_data,
            session_id="temp",
            user_id="temp"
        )

        context = RunContext(deps=deps)

        result = await self.agent.tools["extract_data_from_message"](context, message)
        return result

    async def calculate_progress(self, ctx: RunContext[FormDependencies], form_data: Dict[str, Any]) -> int:
        """Рассчитывает прогресс заполнения."""
        return await self.agent.tools["calculate_progress"](ctx, form_data)

    async def generate_next_question(self, ctx: RunContext[FormDependencies], form_data: Dict[str, Any]) -> str:
        """Генерирует следующий вопрос."""
        return await self.agent.tools["generate_next_question"](ctx, form_data)

    async def detect_user_language(self, ctx: RunContext[FormDependencies], message: str) -> str:
        """Определяет язык пользователя."""
        return await self.agent.tools["detect_user_language"](ctx, message)
```

## Инструменты аналитики

```python
# tools/analytics_base.py
from typing import Dict, Any, List, Optional
import json
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

class BaseAnalyticsTools:
    """
    Базовый класс для аналитических инструментов.
    ВАЖНО: Эти инструменты должны использоваться ТОЛЬКО когда прогресс заполнения формы = 100%.
    Основная задача - анализ заполненных данных формы и предоставление инсайтов.
    """

    def __init__(
        self,
        model: str = "openai/gpt-4o",
        api_key: Optional[str] = None
    ):
        """Инициализирует аналитические инструменты."""
        self.model_name = model
        self.api_key = api_key
        self.client = self._create_client()

    def _create_client(self):
        """Создаёт клиента для запросов к LLM."""
        from openai import AsyncOpenAI

        # Если указан API-ключ, настраиваем клиент
        if self.api_key:
            return AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            # Используем модель с Pydantic AI для демонстрации
            provider = OpenAIProvider(
                base_url="https://api.openai.com/v1",
                api_key="YOUR_API_KEY"
            )

            model = OpenAIModel(
                self.model_name,
                provider=provider
            )

            return model

    async def analyze_form(
        self,
        form_data: Dict[str, Any],
        form_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Анализирует данные формы.
        Используйте этот метод, когда форма полностью заполнена (прогресс = 100%)
        для получения глубокого анализа данных.

        Должен быть переопределён в дочернем классе.
        """
        raise NotImplementedError("Метод analyze_form должен быть переопределён в дочернем классе")

    async def generate_insights(
        self,
        form_data: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> List[str]:
        """
        Генерирует инсайты на основе анализа данных формы.
        Используйте этот метод после анализа формы для получения
        конкретных рекомендаций и выводов.

        Должен быть переопределён в дочернем классе.
        """
        raise NotImplementedError("Метод generate_insights должен быть переопределён в дочернем классе")
```

## Оркестратор инструментов

Оркестратор - это ключевой компонент, который решает, какой инструмент использовать в зависимости от состояния формы.

```python
# core/orchestrator.py
from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel
from pydantic_ai import RunContext

from ..models.dependencies import FormDependencies
from ..models.results import FormResult
from ..models.state import FormState
from ..tools.form_tools import FormTools
from ..tools.analytics_base import BaseAnalyticsTools

class Orchestrator:
    """
    Оркестратор инструментов для обработки форм.
    Решает, какой инструмент использовать в зависимости от прогресса формы:
    - FormTools: если прогресс < 100%
    - AnalyticsTools: если прогресс = 100% и требуется анализ
    """

    def __init__(
        self,
        form_tools: FormTools,
        analytics_tools: Optional[BaseAnalyticsTools] = None
    ):
        """Инициализирует оркестратор инструментов."""
        self.form_tools = form_tools
        self.analytics_tools = analytics_tools

    def _is_analytics_request(self, message: str, form_state: FormState) -> bool:
        """
        Определяет, является ли сообщение запросом на аналитику.

        ВАЖНО: Запрос на аналитику обрабатывается только если форма полностью заполнена
        (прогресс = 100%) и сообщение содержит ключевые слова, связанные с анализом.
        """
        if not form_state.is_complete():
            return False

        if not self.analytics_tools:
            return False

        # Ключевые слова для запроса на аналитику на разных языках
        analytics_keywords = [
            # Русские ключевые слова
            "анализ", "проанализируй", "оцени", "оценка",
            "анализировать", "изучи", "инсайты", "рекомендации",
            # Английские ключевые слова
            "analyze", "assess", "evaluate", "insights", "recommendations",
            "analysis", "review", "examine"
        ]

        return any(keyword in message.lower() for keyword in analytics_keywords)

    async def process(
        self,
        message: str,
        form_state: FormState,
        form_class: Type[BaseModel],
        session_id: str,
        user_id: str,
        message_history: List[Dict[str, Any]]
    ) -> FormResult:
        """
        Обрабатывает сообщение, выбирая между инструментами форм и аналитики.

        Логика выбора:
        1. Если форма заполнена (прогресс = 100%) и сообщение похоже на запрос анализа,
           используем аналитические инструменты
        2. В противном случае используем инструменты формы для заполнения
        """
        # Подготовка зависимостей для инструментов
        deps = FormDependencies(
            form_class=form_class,
            form_data=form_state.form.model_dump(),
            user_id=user_id,
            session_id=session_id,
            progress=form_state.settings.progress,
            message_history=message_history,
            user_language=form_state.settings.language
        )

        # Создаем контекст выполнения
        ctx = RunContext(deps=deps)

        # Определяем язык пользователя (если инструменты формы доступны)
        user_language = deps.user_language
        if message:
            try:
                detected_language = await self.form_tools.detect_user_language(ctx, message)
                if detected_language:
                    user_language = detected_language
            except Exception:
                # Если не удалось определить язык, оставляем текущий
                pass

        # Решаем, какой инструмент использовать
        is_analytics = self._is_analytics_request(message, form_state)

        if form_state.is_complete() and is_analytics and self.analytics_tools:
            # Обработка через аналитические инструменты
            return await self._process_with_analytics(ctx, message, deps)
        else:
            # Обработка через инструменты формы
            return await self._process_with_form_tools(ctx, message, deps, user_language)

    async def _process_with_form_tools(
        self,
        ctx: RunContext[FormDependencies],
        message: str,
        deps: FormDependencies,
        user_language: str
    ) -> FormResult:
        """
        Обрабатывает сообщение с помощью инструментов формы.
        Используется когда форма еще не заполнена полностью (прогресс < 100%).
        """
        # Извлекаем данные из сообщения
        updated_data = await self.form_tools.extract_data_from_message(ctx, message)

        # Рассчитываем прогресс
        progress = await self.form_tools.calculate_progress(ctx, updated_data)

        # Генерируем следующий вопрос
        next_question = await self.form_tools.generate_next_question(ctx, updated_data)

        # Формируем ответ пользователю
        if progress > deps.progress:
            # Если прогресс увеличился, благодарим пользователя
            if user_language == "ru":
                user_message = f"Спасибо за информацию! {next_question}"
            else:
                user_message = f"Thank you for the information! {next_question}"
        else:
            # Если прогресс не изменился, просто задаем следующий вопрос
            user_message = next_question

        return FormResult(
            message=user_message,
            progress=progress,
            next_question=next_question,
            form_update=updated_data,
            user_language=user_language
        )

    async def _process_with_analytics(
        self,
        ctx: RunContext[FormDependencies],
        message: str,
        deps: FormDependencies
    ) -> FormResult:
        """
        Обрабатывает сообщение с помощью аналитических инструментов.
        Используется когда форма полностью заполнена (прогресс = 100%)
        и пользователь запрашивает анализ.
        """
        # Получаем схему формы
        schema = await self.form_tools.get_form_schema(ctx)

        # Анализируем данные формы
        analysis = await self.analytics_tools.analyze_form(
            form_data=deps.form_data,
            form_schema=schema
        )

        # Генерируем инсайты
        insights = await self.analytics_tools.generate_insights(
            form_data=deps.form_data,
            analysis=analysis
        )

        # Формируем ответ пользователю
        if deps.user_language == "ru":
            intro = "Вот результаты анализа:\n\n"
            next_q = "Хотите узнать что-то ещё?"
        else:
            intro = "Here are the analysis results:\n\n"
            next_q = "Would you like to know anything else?"

        # Формируем сообщение с инсайтами
        user_message = intro + "\n".join([f"- {insight}" for insight in insights])

        return FormResult(
            message=user_message,
            progress=100,  # Форма полностью заполнена
            next_question=next_q,
            form_update=deps.form_data,  # Данные не меняются
            user_language=deps.user_language,
            insights=insights
        )
