from typing import Dict, Any, Type, Optional
from pydantic import BaseModel, create_model, Field
import traceback

# Дефолтные значения для различных типов
DEFAULT_VALUES = {
    "string": ("str", ""),
    "integer": ("int", 0),
    "number": ("float", 0.0),
    "boolean": ("bool", False),
    "array": ("list", []),
    "object": ("dict", {}),
}


def generate_default_value(schema: Dict[str, Any]) -> Any:
    """Генерирует дефолтное значение на основе типа в JSON Schema"""
    schema_type = schema.get("type", "string")  # По умолчанию строка
    return DEFAULT_VALUES.get(schema_type, ("Any", None))


def schema_to_model(schema: Dict[str, Any], model_name: Optional[str] = None) -> Type[BaseModel]:
    """
    Конвертирует JSON Schema в Pydantic-модель с дефолтными значениями.

    Args:
        schema: JSON Schema
        model_name: Опциональное имя модели

    Returns:
        Класс Pydantic-модели
    """
    try:
        # Определяем название модели
        final_model_name = model_name or schema.get("title", "DynamicModel")
        final_model_name = "".join(c for c in final_model_name if c.isalnum())

        # Достаём свойства и генерируем аннотации + дефолтные значения
        properties = schema.get("properties", {})
        fields = {
            key: (eval(generate_default_value(value)[0]), Field(default=generate_default_value(value)[1]))
            for key, value in properties.items()
        }

        # Создаём динамическую модель
        model_class = create_model(final_model_name, **fields)

        return model_class
    except Exception as e:
        traceback.print_exc()
        raise e


if __name__ == "__main__":
    schema_example = {
        "title": "User",
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string"},
            "is_active": {"type": "boolean"},
            "roles": {"type": "array"},
            "profile": {
                "type": "object",
                "properties": {
                    "age": {"type": "integer"},
                    "bio": {"type": "string"}
                }
            }
        }
    }

    # Создаём Pydantic-модель из JSON Schema
    UserModel = schema_to_model(schema_example)

    # Создаём экземпляр с дефолтными значениями
    user_instance = UserModel()

    print(user_instance)
