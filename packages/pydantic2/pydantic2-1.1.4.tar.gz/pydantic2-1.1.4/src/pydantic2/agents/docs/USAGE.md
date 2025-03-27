# AIFORMA - Pydantic AI Form Processor

AIFORMA is a powerful Python framework that uses Pydantic models and LLMs (Large Language Models) to automate form collection, validation, and analysis.

## Documentation

For detailed documentation, please refer to:

- [Form Creation Guide](./examples/forms_guide.md) - How to create and use forms
- [Analytics Tools Guide](./analytics_guide.md) - How to use and customize analytics
- [Architecture Overview](./architecture.md) - Technical overview of the framework

## Installation

```bash
pip install aiforma
```

Or from source:

```bash
git clone https://github.com/yourusername/aiforma.git
cd aiforma
pip install -e .
```

## Basic Usage

### Create a Form

Define a form using Pydantic models:

```python
from pydantic import BaseModel, Field

class ContactForm(BaseModel):
    name: str = Field(description="The user's full name")
    email: str = Field(description="The user's email address")
    message: str = Field(description="The message content")
```

### Process the Form

Use the FormProcessor to handle user messages:

```python
from pydantic2.agents import FormProcessor

# Initialize the processor
processor = FormProcessor(
    form_class=ContactForm,
    openrouter_api_key="your_api_key_here"
)

# Process user messages
async def chat():
    response = await processor.process_message("My name is John Smith")
    print(f"Assistant: {response}")

    response = await processor.process_message("My email is john@example.com")
    print(f"Assistant: {response}")

    response = await processor.process_message("I need help with my account")
    print(f"Assistant: {response}")

    # Get the completed form
    form_data = processor.get_form_state()
    print(f"Completed form: {form_data}")

# Run the chat
import asyncio
asyncio.run(chat())
```

## Advanced Analytics

The framework includes powerful analytics capabilities:

```python
from pydantic2.agents import FormProcessor, BaseAnalyticsTools, OpenRouterProvider

# Create custom analytics
class ContactAnalytics(BaseAnalyticsTools):
    def get_analysis_prompt(self, form_data, form_schema):
        return f"""
        Analyze this contact form submission:
        {form_data}

        Return JSON with these fields:
        - sentiment: positive, neutral, or negative
        - priority: high, medium, or low
        - category: the type of inquiry
        """

    def get_insights_prompt(self, form_data, analysis):
        return f"""
        Based on this analysis: {analysis}

        Generate 2 specific recommendations for how to respond to this contact.
        """

# Initialize provider
provider = OpenRouterProvider(api_key="your_api_key")

# Use custom analytics
processor = FormProcessor(
    form_class=ContactForm,
    analytics_tools=ContactAnalytics(provider=provider),
    openrouter_api_key="your_api_key"
)

# Process form and get analytics
async def process_with_analytics():
    # ... process messages ...

    # Form complete! Get insights
    form_data = processor.get_form_state()
    insights = await processor.get_insights()
    print(f"Insights: {insights}")

# Run the processor
asyncio.run(process_with_analytics())
```

## Examples

See the `examples` directory for complete examples:

- `simple_form.py`: Basic form processing
- `startup_form.py`: Complex form with nested structures
- `product_catalog.py`: Form with deeply nested product data
- `resume_builder.py`: Using schema_to_model
- `minimal_analytics.py`: Simple analytics implementation

## Best Practices

1. **Use Field descriptions**: Add clear descriptions to help the LLM understand each field's purpose.
2. **Leverage validation**: Use Pydantic's validation features to ensure data quality.
3. **Group related fields**: Use nested models to organize complex forms.
4. **Design clear prompts**: When creating custom analytics, focus on prompt design.
5. **Save sessions**: For longer forms, save the session ID and form state between user interactions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
