# Pydantic AI Form Processor - Схемы и Диаграммы

> Визуализация процессов, архитектуры и потоков данных системы интеллектуального заполнения форм

## Общая архитектура системы

```mermaid
flowchart TD
    User([Пользователь]) <-->|Сообщения| FP[FormProcessor]

    subgraph "Основные компоненты"
        FP --> Orch[Оркестратор]
        Orch --> FT[FormTools]
        Orch --> AT[AnalyticsTools]
        FP <--> SM[SessionManager]
    end

    subgraph "Хранение данных"
        SM <--> DB[(База данных)]
    end

    subgraph "Внешние сервисы"
        FT <--> LLM1[OpenRouter LLM]
        AT <--> LLM2[OpenRouter LLM]
        Orch <--> LLM3[OpenRouter LLM]
    end

    classDef user fill:#f96,stroke:#333,stroke-width:2px
    classDef core fill:#9cf,stroke:#333,stroke-width:1px
    classDef db fill:#b9d,stroke:#333,stroke-width:1px
    classDef external fill:#9f9,stroke:#333,stroke-width:1px

    class User user
    class FP,Orch,FT,AT,SM core
    class DB db
    class LLM1,LLM2,LLM3 external
```

## Процесс обработки сообщений

```mermaid
sequenceDiagram
    participant User as Пользователь
    participant FP as FormProcessor
    participant SM as SessionManager
    participant Orch as Оркестратор
    participant FT as FormTools
    participant AT as AnalyticsTools
    participant LLM as LLM

    User->>FP: Отправляет сообщение

    FP->>SM: Получить/создать сессию
    SM->>FP: Данные сессии

    FP->>Orch: Обработать сообщение

    alt Форма не заполнена (прогресс < 100%)
        Orch->>FT: Извлечь данные из сообщения
        FT->>LLM: Запрос на извлечение данных
        LLM->>FT: Обновленные данные формы

        FT->>LLM: Запрос на расчет прогресса
        LLM->>FT: Процент заполнения

        FT->>LLM: Запрос на генерацию вопроса
        LLM->>FT: Следующий вопрос

        FT->>Orch: Результат обработки
    else Форма заполнена (прогресс = 100%)
        Orch->>AT: Проанализировать данные формы
        AT->>LLM: Запрос на анализ данных
        LLM->>AT: Результаты анализа

        AT->>LLM: Запрос на генерацию инсайтов
        LLM->>AT: Инсайты

        AT->>Orch: Результаты и инсайты
    end

    Orch->>FP: Результат обработки

    FP->>SM: Сохранить обновленное состояние

    FP->>User: Ответ (вопрос/инсайты)
```

## Процесс сессионного управления

```mermaid
sequenceDiagram
    participant User as Пользователь
    participant FP as FormProcessor
    participant SM as SessionManager
    participant DB as База данных

    alt Новая сессия
        User->>FP: Первое сообщение
        FP->>SM: Создать сессию (user_id)
        SM->>DB: Сохранить сессию
        SM->>FP: ID сессии
        FP->>User: Первый вопрос
    else Продолжение существующей сессии
        User->>FP: Сообщение + session_id
        FP->>SM: Найти сессию (session_id)
        SM->>DB: Запрос сессии
        DB->>SM: Данные сессии
        SM->>FP: Состояние формы
        FP->>User: Ответ на основе состояния
    end
```

## Извлечение данных и работа с многомерными структурами

```mermaid
flowchart TD
    Message[Сообщение пользователя] --> DetectStructure{Определить сложность данных}

    DetectStructure -->|Простые данные| JSON[JSON обработка]
    DetectStructure -->|Сложные многомерные данные| YAML[YAML обработка]

    JSON --> Extract1[Извлечение данных через LLM]
    YAML --> Extract2[Извлечение данных через LLM]

    Extract1 --> Merge[Слияние с существующими данными]
    Extract2 --> Merge

    Merge --> Update[Обновление формы]

    subgraph "Многоуровневое обновление"
        Update --> Field1[Обновление простых полей]
        Update --> Lists[Объединение списков]
        Update --> Nested[Рекурсивное обновление вложенных объектов]
    end
```

## Архитектура данных

```mermaid
erDiagram
    Session ||--o{ State : "содержит"
    Session ||--o{ Message : "содержит"

    Session {
        string session_id PK
        string user_id
        string client_id
        string form_class
        datetime created_at
    }

    State {
        int id PK
        string session_id FK
        json data
        datetime created_at
    }

    Message {
        int id PK
        string session_id FK
        string role
        text content
        datetime created_at
    }
```

## Процесс создания и обработки формы

```mermaid
stateDiagram-v2
    [*] --> Initialization: Создание сессии

    Initialization --> FormFilling: Начальный вопрос

    state FormFilling {
        [*] --> ExtractData: Сообщение пользователя
        ExtractData --> CalculateProgress: Обновление данных
        CalculateProgress --> GenerateQuestion: Расчет прогресса
        GenerateQuestion --> [*]: Следующий вопрос
    }

    FormFilling --> FormCompleted: Прогресс достиг 100%

    state FormCompleted {
        [*] --> Analysis: Запрос анализа
        Analysis --> GenerateInsights: Результаты анализа
        GenerateInsights --> [*]: Инсайты
    }

    FormCompleted --> [*]: Завершение
```

## Преобразование моделей и интеграция с внешними системами

```mermaid
flowchart TD
    subgraph "Django / Внешняя система"
        M1[Django модель/данные] --> S1[JSON-схема]
    end

    subgraph "Pydantic AI Form Processor"
        S1 --> Convert[schema_to_model]
        Convert --> PyM[Pydantic модель]

        PyM --> FormP[FormProcessor]
        FormP --> Result[Заполненная форма]

        Result --> S2[model_json_schema]
        S2 --> PyDict[Python словарь]
    end

    subgraph "Обратная интеграция"
        PyDict --> M2[Django модель/данные]
    end
```

## Обработка многомерных данных с использованием YAML

```mermaid
flowchart LR
    subgraph "Входные данные"
        I1[Многомерная модель]
    end

    subgraph "Преобразование"
        I1 --> ModelDump[model_dump]
        ModelDump --> Y1[YAML представление]

        Y1 --> LLM[LLM обработка]

        LLM --> Y2[Обновленный YAML]
        Y2 --> SafeLoad[yaml.safe_load]
        SafeLoad --> Dict[Python словарь]
    end

    subgraph "Результат"
        Dict --> Validate[Валидация данных]
        Validate --> O1[Обновленная Pydantic модель]
    end

    style I1 fill:#f96,stroke:#333
    style O1 fill:#9f9,stroke:#333
    style LLM fill:#9cf,stroke:#333,stroke-width:2px
```

## Взаимодействие компонентов в FormProcessor

```mermaid
classDiagram
    class FormProcessor {
        +SessionManager session_manager
        +FormTools form_tools
        +AnalyticsTools analytics_tools
        +Orchestrator orchestrator
        +initialize(user_id, session_id) session_id, first_question
        +process_message(message, session_id) FormResult
        +create_session(user_id, form_data) session_id
        +save_message(session_id, role, content)
    }

    class SessionManager {
        +create_session(user_id, form_class)
        +get_session(session_id)
        +save_state(session_id, state_data)
        +save_message(session_id, role, content)
        +get_messages(session_id)
        +get_state_history(session_id)
        +debug_session_info(session_id)
        +check_database()
    }

    class Orchestrator {
        +process(message, form_state, form_class, session_id, user_id, message_history)
        -_process_with_form_tools()
        -_process_with_analytics()
        -_is_analytics_request()
    }

    class FormTools {
        +get_form_schema(form_class)
        +extract_data_from_message(message, form_data, form_class)
        +calculate_progress(ctx, form_data)
        +generate_next_question(ctx, form_data)
        +detect_user_language(ctx, message)
        +extract_data_from_yaml(ctx, message)
    }

    class BaseAnalyticsTools {
        +analyze_form(form_data, form_schema)
        +generate_insights(form_data, analysis)
    }

    FormProcessor --> SessionManager
    FormProcessor --> Orchestrator
    Orchestrator --> FormTools
    Orchestrator --> BaseAnalyticsTools
```

## Модель тестирования через тест-агенты

```mermaid
sequenceDiagram
    participant FP as FormProcessor
    participant TA as TestAgent
    participant FT as FormTools
    participant SM as SessionManager

    FP->>FP: configure_test_agent()
    FP->>SM: initialize()
    SM->>FP: session_id, first_question

    loop Для каждого диалогового шага
        FP->>TA: Сгенерировать ответ пользователя
        TA->>FP: Симулированное сообщение пользователя

        FP->>FT: process_message()
        FT->>FP: Результат обработки

        FP->>SM: Сохранить сообщения и состояние

        alt Форма заполнена
            FP->>FP: Проверка completion_achieved

            alt auto_continue=false
                FP->>FP: Завершить тестирование
            end
        end
    end

    FP->>FP: Сформировать отчет о тестировании
```
