from typing import Type, TypeVar
from pydantic import BaseModel
from polyfactory.factories.pydantic_factory import ModelFactory
from faker import Faker

T = TypeVar("T", bound=BaseModel)

class UniversalModelFactory:
    """Factory for generating Pydantic models with or without fake data."""

    def __init__(self, model: Type[T], fill_data: bool = False):
        if not issubclass(model, BaseModel):
            raise ValueError("Provided model must be a subclass of Pydantic BaseModel")

        self.model = model
        self.fill_data = fill_data
        self.factory = self._create_factory()

    def _create_factory(self):
        """Dynamically creates a factory for the given model."""
        faker_instance = Faker("en_US")
        faker_instance.seed_instance(42)  # Ensures reproducibility

        class DynamicFactory(ModelFactory[self.model]):  # ✅ ПРАВИЛЬНО
            __model__ = self.model
            __faker__ = faker_instance

        return DynamicFactory()  # Создаём экземпляр фабрики

    def _clear_data(self, data: dict, model_cls: Type[BaseModel]) -> dict:
        """Recursively replaces values with empty equivalents."""
        cleared_data = {}
        for key, value in data.items():
            field_type = model_cls.__annotations__.get(key, None)

            if isinstance(value, str):
                cleared_data[key] = ""
            elif isinstance(value, list):
                cleared_data[key] = []
            elif isinstance(value, dict):
                cleared_data[key] = {}
            elif isinstance(value, BaseModel) and field_type:
                cleared_data[key] = field_type(**self._clear_data(value.model_dump(), field_type))
            else:
                cleared_data[key] = value  # Keep default for numbers, booleans, etc.
        return cleared_data

    def build(self) -> T:
        """Creates a model instance with fake or empty data."""
        instance = self.factory.build()
        if not self.fill_data:
            return self.model(**self._clear_data(instance.model_dump(), self.model))
        return instance


if __name__ == "__main__":
    class Address(BaseModel):
        city: str
        street: str

    class User(BaseModel):
        id: int
        email: str
        name: str
        address: Address

    user_with_data = UniversalModelFactory(User, fill_data=True).build()
    print(f"Filled model: {user_with_data}")

    empty_user = UniversalModelFactory(User, fill_data=False).build()
    print(f"Empty model: {empty_user}")
