# Pydantic AI Form Processor - Usage Guide

## Basic Usage

### Installation

```bash
# The library uses OpenAI, peewee, and pydantic
pip install openai peewee pydantic faker pyyaml
```

### Simple Form

```python
import asyncio
from pydantic import BaseModel, Field
from pydantic2.agents import FormProcessor

# Define your form
class ContactForm(BaseModel):
    name: str = Field(default="", description="Contact name")
    email: str = Field(default="", description="Email address")
    message: str = Field(default="", description="Message content")

async def main():
    # Create processor
    processor = FormProcessor(
        form_class=ContactForm,
        openrouter_api_key="your_api_key_here"
    )

    # Initialize session
    session_id, first_question = await processor.initialize()
    print(f"Assistant: {first_question}")

    # Process messages
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        result = await processor.process_message(user_input, session_id)
        print(f"Assistant: {result.message}")
        print(f"Progress: {result.progress}%")

        if result.completion_achieved:
            print("\nForm completed!")
            state = await processor.get_form_state()
            print(f"Final data: {state.form}")
            break

if __name__ == "__main__":
    asyncio.run(main())
```

## Form with Nested Structure

```python
from pydantic import BaseModel, Field

# Nested model
class Address(BaseModel):
    street: str = Field(default="", description="Street address")
    city: str = Field(default="", description="City")
    zipcode: str = Field(default="", description="Postal/ZIP code")

# Main form with nested field
class UserProfile(BaseModel):
    name: str = Field(default="", description="Full name")
    email: str = Field(default="", description="Email address")
    address: Address = Field(default_factory=Address, description="Mailing address")
    occupation: str = Field(default="", description="Current occupation")
```

The system automatically handles nested models, extracting the full structure from user messages.

## Custom Analytics

```python
from pydantic2.agents import BaseAnalyticsTools, OpenRouterProvider

class UserProfileAnalytics(BaseAnalyticsTools):
    async def analyze_form(self, form_data, form_schema):
        """Analyze a completed user profile form."""
        system_prompt = f"""
        Analyze this user profile and generate a standardized assessment.

        USER PROFILE:
        ```json
        {form_data}
        ```

        Generate a detailed analysis with these categories:
        1. User background summary
        2. Communication preferences
        3. Location analysis

        Return as JSON with these three fields.
        """

        result = await self.provider.invoke(
            system=system_prompt,
            user="",
            temperature=0.7,
            response_format={"type": "json_object"}
        )

        return result.choices[0].message.content

    async def generate_insights(self, form_data, analysis):
        """Generate insights based on the analysis."""
        system_prompt = f"""
        Generate 3-5 useful insights based on this user profile analysis.

        ANALYSIS:
        ```json
        {analysis}
        ```

        Each insight should be a clear, actionable recommendation.
        """

        result = await self.provider.invoke(
            system=system_prompt,
            user="",
            temperature=0.7
        )

        # Split into separate insights
        insights = [line.strip() for line in result.choices[0].message.content.split("\n") if line.strip()]
        return insights

# Create with provider
provider = OpenRouterProvider(api_key="your_api_key")
analytics = UserProfileAnalytics(provider=provider)

# Use with form processor
processor = FormProcessor(
    form_class=UserProfile,
    analytics_tools=analytics,
    openrouter_api_key="your_api_key"
)
```

## Working with JSON Schemas

If you need to convert a JSON schema to a Pydantic model:

```python
from pydantic2.agents import schema_to_model

# Example schema (perhaps from Django or another system)
schema = {
    "title": "ProductForm",
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "Product name"},
        "price": {"type": "number", "description": "Product price"},
        "categories": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Product categories"
        }
    }
}

# Convert to Pydantic model
ProductForm = schema_to_model(schema)

# Use with processor
processor = FormProcessor(form_class=ProductForm, openrouter_api_key="your_api_key")
```

## Generating Test Data

To generate test data for your forms:

```python
from pydantic2.agents import UniversalModelFactory

# Create factory
factory = UniversalModelFactory(UserProfile)

# Generate test data
test_user = factory.build()
print(test_user.model_dump())

# Override specific fields
custom_user = factory.generate(
    UserProfile,
    name="Jane Smith",
    email="jane@example.com"
)
```

## Environment Variables

For security, use environment variables for API keys:

```python
import os
from pydantic2.agents import FormProcessor

# Get API key from environment
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENROUTER_API_KEY environment variable")

# Create processor with environment API key
processor = FormProcessor(form_class=YourForm, openrouter_api_key=api_key)
```
