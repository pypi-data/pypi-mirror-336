# Form Creation Guide

This guide explains how to create and use forms with the Pydantic AI Form Processor.

## Overview

Forms in the Pydantic AI Form Processor are based on Pydantic models, which provide robust validation, serialization, and documentation. The `FormTools` class helps manage the form-filling process by tracking progress, validating inputs, and providing helpful feedback.

## Creating a Form

### Basic Form

A basic form is just a Pydantic model:

```python
from pydantic import BaseModel, Field

class SimpleForm(BaseModel):
    name: str = Field(description="The user's full name")
    age: int = Field(description="The user's age in years", gt=0, lt=120)
    email: str = Field(description="The user's email address")
    interests: list[str] = Field(description="A list of the user's interests")
```

### Nested Forms

Forms can contain nested models for complex data structures:

```python
class Address(BaseModel):
    street: str = Field(description="Street address")
    city: str = Field(description="City name")
    state: str = Field(description="State or province")
    zip_code: str = Field(description="Postal/zip code")

class UserProfile(BaseModel):
    name: str = Field(description="User's full name")
    address: Address = Field(description="User's mailing address")
    phone: str = Field(description="User's phone number")
```

### Form with Constraints

Use Pydantic's validation features to enforce data constraints:

```python
from pydantic import BaseModel, Field, EmailStr, constr

class RegistrationForm(BaseModel):
    username: constr(min_length=3, max_length=20) = Field(
        description="Username (3-20 characters)"
    )
    email: EmailStr = Field(description="Valid email address")
    password: constr(min_length=8) = Field(
        description="Password (at least 8 characters)"
    )
    terms_accepted: bool = Field(
        description="User has accepted the terms of service"
    )
```

## Using Schema to Model Utility

For complex forms, you can define a JSON schema and convert it to a Pydantic model:

```python
from pydantic2.agents17.utils import schema_to_model

resume_schema = {
    "type": "object",
    "properties": {
        "personal_info": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Full name"},
                "email": {"type": "string", "description": "Email address"},
                "phone": {"type": "string", "description": "Phone number"}
            },
            "required": ["name", "email"]
        },
        "experience": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "company": {"type": "string"},
                    "position": {"type": "string"},
                    "start_date": {"type": "string"},
                    "end_date": {"type": "string"}
                }
            }
        }
    }
}

ResumeForm = schema_to_model("ResumeForm", resume_schema)
```

## Form Processing

### Basic Usage with FormProcessor

```python
from pydantic2.agents17 import FormProcessor

# Initialize processor
processor = FormProcessor(
    form_class=UserProfile,
    openrouter_api_key="your_api_key"
)

# Process a user message
response = await processor.process_message("My name is John Smith")

# Get current form state
current_state = processor.get_form_state()
```

### Custom Logic with FormTools

For direct access to form tools:

```python
from pydantic2.agents17 import FormTools, OpenRouterProvider

# Initialize provider
provider = OpenRouterProvider(api_key="your_api_key")

# Create form tools
form_tools = FormTools(form_class=UserProfile, provider=provider)

# Process a message
result = await form_tools.process_message("I live at 123 Main St, Springfield")

# Check completion progress
completion = form_tools.get_completion_percentage()
print(f"Form is {completion}% complete")

# Get current form data
current_data = form_tools.get_current_data()
```

## Form Validation

The processor automatically validates data as it's collected. When validation fails, it will ask for corrections.

Example validation errors:

```
- For 'age': Input should be greater than 0
- For 'email': Input is not a valid email address
```

## Best Practices

1. **Be Descriptive**: Use Field descriptions to provide context for the AI
2. **Use Validation**: Leverage Pydantic validation for cleaner data
3. **Group Related Fields**: Use nested models to organize related data
4. **Document Requirements**: Specify required vs optional fields clearly
5. **Handle Incomplete Data**: Check completion percentage before finalizing

## Advanced Features

### Custom Field Processing

You can override how specific fields are processed:

```python
class CustomFormTools(FormTools):
    async def process_field_value(self, field_name, user_message, field_info):
        # Custom processing for specific fields
        if field_name == "special_field":
            # Custom validation or transformation
            return processed_value

        # Fall back to default processing
        return await super().process_field_value(field_name, user_message, field_info)
```

### Saving and Resuming Forms

Use session management to save and resume form filling:

```python
# Save form state
session_id = processor.get_session_id()
form_state = processor.get_form_state()

# Later, resume with saved state
resumed_processor = FormProcessor(
    form_class=UserProfile,
    openrouter_api_key="your_api_key",
    session_id=session_id,
    form_state=form_state
)
```

## Example Walkthrough

See the example files like `simple_form.py`, `startup_form.py`, and `product_catalog.py` for complete examples of form processing from beginning to end.
