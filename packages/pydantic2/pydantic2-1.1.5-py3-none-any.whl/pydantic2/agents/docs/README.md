# AIFORMA - Pydantic AI Form Processor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful framework for creating AI-powered form processing applications using Pydantic models and Large Language Models.

## Features

- 🧠 **AI-Powered Form Filling**: Uses LLMs to intelligently extract information from natural language
- ✅ **Validation Built-in**: Leverages Pydantic's robust validation system
- 🔄 **State Management**: Tracks form completion progress and manages user sessions
- 📊 **Analytics & Insights**: Analyzes completed forms and generates actionable insights
- 📚 **Flexible Schema**: Support for complex nested data structures and arrays
- 🔌 **Pluggable Providers**: Easily switch between different LLM providers

## Quick Example

```python
from pydantic import BaseModel, Field
from pydantic2.agents import FormProcessor

class SimpleForm(BaseModel):
    name: str = Field(description="The user's full name")
    age: int = Field(description="The user's age in years")

processor = FormProcessor(
    form_class=SimpleForm,
    openrouter_api_key="your_api_key"
)

async def main():
    # Process messages
    response = await processor.process_message("My name is John Smith")
    print(response)  # The assistant will ask for age

    response = await processor.process_message("I'm 32 years old")
    print(response)  # The assistant will confirm the form is complete

    # Get form data
    form_data = processor.get_form_state()
    print(form_data)  # {'name': 'John Smith', 'age': 32}

import asyncio
asyncio.run(main())
```

## Documentation

For detailed documentation, please refer to:

- [Usage Guide](./USAGE.md) - Introduction and basic usage
- [Form Creation Guide](./examples/forms_guide.md) - How to create and use forms
- [Analytics Tools Guide](./analytics_guide.md) - How to use and customize analytics
- [Architecture Overview](./architecture.md) - Technical overview of the framework
- [Examples](./examples/) - Complete examples demonstrating various features:
  - [Simple Form](./examples/simple_form.py) - Basic form processing
  - [Startup Form](./examples/startup_form.py) - Complex nested form
  - [Product Catalog](./examples/product_catalog.py) - Multi-level nested structures
  - [Resume Builder](./examples/resume_builder.py) - Using schema_to_model
  - [Minimal Analytics](./examples/minimal_analytics.py) - Simple analytics example

## Key Components

### FormProcessor
Main entry point for applications, handling sessions and orchestrating form processing.

### FormTools
Core form filling engine, extracting and validating data from user messages.

### BaseAnalyticsTools
Template-based system for analyzing completed forms and generating insights.

### LLM Providers
Interchangeable providers for different LLM services (OpenRouter, Claude, etc).

## Requirements

- Python 3.9+
- OpenRouter API key or other supported LLM provider key

## Installation

```bash
pip install aiforma
```

## License

MIT License
