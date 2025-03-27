#!/usr/bin/env python3
"""
Django API Test Example

This script simulates how Django uses the FormProcessor and shows serialization issues.
"""

import os
import json
import asyncio
from typing import Dict, Any, Optional
from pprint import pprint
from pydantic import BaseModel, Field

# Add parent directory to path
import sys
import pathlib
parent_dir = str(pathlib.Path(__file__).parent.parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from pydantic2.agents import FormProcessor
from pydantic2.agents.models.state import FormState, Settings


# Define a simple form model for testing
class TestPersonForm(BaseModel):
    """Test person form for serialization testing."""
    name: str = Field(default="", description="Person's full name")
    age: Optional[int] = Field(default=None, description="Person's age")
    email: Optional[str] = Field(default=None, description="Email address")
    address: Optional[str] = Field(default=None, description="Home address")


# Simulate Django processor
class DjangoProcessor:
    """Simulates the DjangoFormProcessor in Django."""

    def __init__(self):
        # Get API key from environment
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")

        # Create the actual form processor
        self.processor = FormProcessor(
            form_class=TestPersonForm,
            openrouter_api_key=api_key,
            model="openai/gpt-4o-mini",
            client_id="test_client",
            verbose=True
        )

        # Session ID
        self.session_id = None

    async def initialize(self) -> Dict[str, Any]:
        """Initialize a session."""
        session_id, welcome_msg = await self.processor.initialize(
            user_id="test_user",
            session_id=None,
            initial_data=None
        )

        self.session_id = session_id

        return {
            "session_id": session_id,
            "message": welcome_msg
        }

    async def process_message(self, message: str) -> Dict[str, Any]:
        """Process a user message."""
        result = await self.processor.process_message(message, self.session_id)
        return result

    async def get_form_state(self) -> Dict[str, Any]:
        """Get form state."""
        form_state = await self.processor.get_form_state(self.session_id)
        return form_state

    async def get_messages(self) -> Dict[str, Any]:
        """Get messages."""
        history = await self.processor.get_session_history(self.session_id)
        return history.get("messages", [])


# Testing functions
async def test_serialization(proc: DjangoProcessor):
    """Test serialization of FormState."""
    form_state = await proc.get_form_state()

    print("=== Original Form State Object ===")
    print(f"Type: {type(form_state)}")
    print(f"Form type: {type(form_state.form)}")
    print(f"Form attributes: {dir(form_state.form)}")

    print("\n=== State.__repr__() ===")
    print(repr(form_state))

    print("\n=== Python dict ===")
    # Direct model_dump
    print("FormState.model_dump():")
    state_dict = form_state.model_dump()
    pprint(state_dict)

    # Manual extraction
    print("\nManual dict construction:")
    manual_dict = {
        "form": form_state.get_form_json(),
        "settings": form_state.settings.model_dump(),
    }
    pprint(manual_dict)

    print("\n=== JSON Serialization ===")
    # JSON dumps from model_dump
    print("json.dumps(FormState.model_dump()):")
    state_json = json.dumps(form_state.model_dump())
    print(state_json)

    print("\nMockup of Django Response:")
    response_data = {
        "session_id": proc.session_id,
        "history": await proc.get_messages(),
        "current_state": form_state.model_dump()
    }
    print(json.dumps(response_data))

    print("\n=== Deserialization Test ===")
    # Simulate what DRF might do during serialization
    print("DRF-like serialization process:")
    drf_serialized = json.loads(json.dumps(response_data))
    pprint(drf_serialized)


async def main():
    """Run the test."""
    print("Initializing Django processor...")
    proc = DjangoProcessor()

    print("Creating session...")
    init_result = await proc.initialize()
    print(f"Session created: {init_result['session_id']}")

    # Проверим исходное состояние формы
    print("\nInitial form state:")
    form_state_before = await proc.get_form_state()
    print(f"Form state type: {type(form_state_before)}")
    print(f"Form state content: {form_state_before}")

    # Отправим короткое сообщение с именем - как имитация сообщения "Марк"
    print("\nSending simple name message...")
    name_message = "Марк"
    name_result = await proc.process_message(name_message)
    if hasattr(name_result, 'get'):
        response = name_result.get('response')
        if hasattr(response, 'form_update'):
            print(f"Form update received: {response.form_update}")

    # Проверим состояние формы после сообщения с именем
    print("\nForm state after name message:")
    form_state_after_name = await proc.get_form_state()
    print(f"Form state type: {type(form_state_after_name)}")
    print(f"Form state content: {form_state_after_name}")
    print(f"Form content: {form_state_after_name.form if hasattr(form_state_after_name, 'form') else 'No form attribute'}")

    # Отправим сообщение с email
    print("\nSending email message...")
    email_message = "test@example.com"
    email_result = await proc.process_message(email_message)

    # Проверим состояние формы после сообщения с email
    print("\nForm state after email message:")
    form_state_after_email = await proc.get_form_state()
    print(f"Form content: {form_state_after_email.form if hasattr(form_state_after_email, 'form') else 'No form attribute'}")

    # Отправим многословное сообщение
    print("\nSending complex message...")
    message = "My name is John Doe, I'm 35 years old, and my email is john@example.com"
    await proc.process_message(message)

    # Проверим состояние формы после сложного сообщения
    print("\nForm state after complex message:")
    form_state_after = await proc.get_form_state()
    print(f"Form content: {form_state_after.form if hasattr(form_state_after, 'form') else 'No form attribute'}")

    # Test serialization
    print("\nTesting serialization...\n")
    await test_serialization(proc)

    # Проверим JSON-сериализацию, имитирующую API ответ
    print("\nSimulating API response...")
    form_state = await proc.get_form_state()

    # Прямая сериализация
    form_state_dict = {}
    if hasattr(form_state, 'model_dump'):
        form_state_dict = form_state.model_dump()
    else:
        # Ручное преобразование
        if hasattr(form_state, 'form'):
            form_state_dict['form'] = form_state.form.model_dump() if hasattr(form_state.form, 'model_dump') else form_state.form
        if hasattr(form_state, 'settings'):
            form_state_dict['settings'] = form_state.settings.model_dump() if hasattr(form_state.settings, 'model_dump') else form_state.settings

    print("\nAPI Response Simulation:")
    api_response = {
        'session_id': proc.session_id,
        'current_state': {
            'form': form_state_dict.get('form', {}),
            'settings': form_state_dict.get('settings', {})
        }
    }
    print(f"API response: {api_response}")

    # Проверим, записывается ли что-то в форму
    form_content = api_response['current_state']['form']
    if not form_content:
        print("\n⚠️ ПРЕДУПРЕЖДЕНИЕ: Данные формы пусты! Это похоже на проблему, которую мы видим в API.")
    else:
        print(f"\n✅ Форма содержит данные: {form_content}")


if __name__ == "__main__":
    asyncio.run(main())
