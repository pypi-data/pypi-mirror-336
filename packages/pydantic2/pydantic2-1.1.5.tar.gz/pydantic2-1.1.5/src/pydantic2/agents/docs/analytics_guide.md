# Analytics Tools Guide

This guide explains how to use the analytics tools in the Pydantic AI Form Processor.

## Overview

The `BaseAnalyticsTools` class provides a simple and flexible way to analyze completed forms and generate insights based on that analysis. It uses a template method pattern that makes it easy to create custom analytics for specific form types.

## Quick Start

Creating a custom analytics tool is as simple as inheriting from `BaseAnalyticsTools` and overriding the prompt methods:

```python
from pydantic2.agents import BaseAnalyticsTools

class MyAnalytics(BaseAnalyticsTools):
    def get_analysis_prompt(self, form_data, form_schema):
        return f"""
        Analyze this data: {json.dumps(form_data)}

        Return analysis as JSON with these fields:
        - quality_score
        - key_points
        - recommendations
        """

    def get_insights_prompt(self, form_data, analysis):
        return f"""
        Based on this analysis: {json.dumps(analysis)}

        Generate 3 specific recommendations.
        """
```

That's it! The base class handles all the LLM interactions, error handling, and formatting.

## Key Features

- **Template Method Pattern**: Only override what you need
- **Automatic Error Handling**: Graceful recovery from API issues
- **Standardized Output Processing**: Consistent insight formatting
- **Customizable Defaults**: Override default values for error cases

## Core Methods

### Template Methods (Override These)

1. **`get_analysis_prompt(self, form_data, form_schema) -> str`**:
   - Override to customize the system prompt for analysis
   - Returns a string containing the prompt

2. **`get_insights_prompt(self, form_data, analysis) -> str`**:
   - Override to customize the system prompt for insights generation
   - Returns a string containing the prompt

3. **`get_default_analysis_result(self, form_data, error_message) -> Dict`**:
   - Override to customize the fallback response when analysis fails
   - Returns a dictionary with default analysis fields

4. **`get_default_insights(self, error_message) -> List[str]`**:
   - Override to customize the fallback insights when generation fails
   - Returns a list of strings

5. **`format_insights(self, insights) -> List[str]`**:
   - Override to customize how raw insights are formatted
   - Returns a list of strings

### Core Methods (Use These)

1. **`analyze_form(self, form_data, form_schema) -> Dict`**:
   - Analyzes form data using LLM with your custom prompt
   - Returns a dictionary with analysis results

2. **`generate_insights(self, form_data, analysis) -> List[str]`**:
   - Generates insights based on analysis using LLM with your custom prompt
   - Returns a list of strings containing insights

## Example Usage

```python
# Initialize provider
provider = OpenRouterProvider(api_key="your_api_key")

# Create analytics
analytics = MyAnalytics(provider=provider)

# Use with FormProcessor
processor = FormProcessor(
    form_class=MyForm,
    analytics_tools=analytics,
    openrouter_api_key="your_api_key"
)
```

## Complete Example

See the `minimal_analytics.py` example for a minimal implementation or check other examples like `startup_form.py` and `resume_builder.py` for more complex implementations.

## Best Practices

1. **Focus on prompts**: The key to good analytics is well-designed prompts
2. **Use schema information**: Incorporate form schema in your prompts for better context
3. **Handle domain-specific errors**: Provide meaningful defaults for your domain
4. **Format insights consistently**: Use the template methods for consistent output

## Advanced Usage

For more advanced analytics, you can completely override the core methods:

```python
class AdvancedAnalytics(BaseAnalyticsTools):
    async def analyze_form(self, form_data, form_schema):
        # Custom implementation that doesn't use LLM
        # or uses multiple LLM calls
        return custom_analysis

    async def generate_insights(self, form_data, analysis):
        # Custom implementation
        return custom_insights
```

This gives you complete control when needed, while still maintaining a consistent interface.
