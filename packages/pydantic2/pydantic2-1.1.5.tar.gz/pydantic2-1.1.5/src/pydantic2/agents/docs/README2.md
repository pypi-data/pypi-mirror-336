# Pydantic AI Form Processor (agents17)

> A simplified framework for intelligent form processing with LLMs

## Overview

This is a streamlined implementation of the Pydantic AI Form Processor, designed for intelligent form processing with minimal code complexity. Key features:

1. **Conversational Form Filling** - Guide users through forms with natural language
2. **Structured Data Extraction** - Extract data from free-text responses
3. **Session Management** - Support long-running conversations with persistence
4. **Analytics Generation** - Analyze completed forms and generate insights
5. **OpenRouter Integration** - Access to powerful LLMs through OpenRouter

## Implementation Highlights

- **Clean Architecture** - Clear separation of concerns with minimal dependencies
- **Efficient Form Tools** - Leverages LLMs for all intelligence tasks
- **Peewee ORM** - Simple database interactions for session management
- **Pydantic Integration** - Full support for nested models and JSON schema
- **Faker Integration** - Smart test data generation based on field descriptions

## Usage Example

```python
import asyncio
from pydantic import BaseModel, Field
from pydantic2.agents import FormProcessor

# Define your form model
class SimpleForm(BaseModel):
    name: str = Field(default="", description="Your name")
    age: int = Field(default=0, description="Your age")
    interests: list[str] = Field(default_factory=list, description="Your interests")

async def main():
    # Create form processor
    processor = FormProcessor(
        form_class=SimpleForm,
        openrouter_api_key="your_api_key"
    )

    # Initialize session
    session_id, first_question = await processor.initialize()
    print(f"First question: {first_question}")

    # Process a message
    result = await processor.process_message(
        "My name is Alice and I'm 28 years old",
        session_id
    )
    print(f"Progress: {result.progress}%")
    print(f"Response: {result.message}")

    # Process another message
    result = await processor.process_message(
        "I'm interested in AI, music, and hiking",
        session_id
    )

    # Check if form is complete
    if result.completion_achieved:
        state = await processor.get_form_state()
        print("Form data:", state.form)

asyncio.run(main())
```

## Key Components

### FormProcessor

The main entry point, coordinating all other components and providing a simple API.

### FormTools

Provides LLM-powered capabilities for:
- Extracting data from user messages
- Calculating form completion progress
- Generating relevant questions

### Orchestrator

Decides which tools to use based on the form state:
- Form tools for data extraction and question generation
- Analytics tools for completed forms

### SessionManager

Handles persistence using Peewee ORM:
- Storing session information
- Saving form state history
- Tracking message history

### OpenRouterProvider

Provides access to powerful LLMs through the OpenRouter API:
- Uses the standard OpenAI client interface
- Support for various models via model name parameter
- Simple implementation with appropriate defaults

## For Developers

- All tools leverage LLMs for the intelligent components
- Form extraction automatically adapts to simple vs complex forms
- JSON is used for simple forms, YAML for forms with nested structures
- The system automatically handles merging of form data with special care for lists
- Test data generation is available through the UniversalModelFactory with Faker integration
