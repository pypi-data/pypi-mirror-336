#!/usr/bin/env python
"""
Simple form example for the Pydantic AI Form Processor.
"""

import os
import asyncio
from typing import List
from pydantic import BaseModel, Field
import json

# Import from our library
from pydantic2.agents import FormProcessor
from pydantic2.agents import BaseAnalyticsTools, OpenRouterProvider

# Get API key from environment
API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("Please set the OPENROUTER_API_KEY environment variable")

# Define a simple form
class SimpleForm(BaseModel):
    name: str = Field(default="", description="User's full name")
    age: int = Field(default=0, description="User's age in years")
    occupation: str = Field(default="", description="User's current job or occupation")
    interests: List[str] = Field(default_factory=list, description="User's hobbies and interests")
    goals: str = Field(default="", description="User's professional or personal goals")

# Simple analytics implementation
class SimpleAnalytics(BaseAnalyticsTools):
    def get_analysis_prompt(self, form_data, form_schema):
        """Customize system prompt for personal profile analysis."""
        return f"""
        Analyze this personal profile data and generate a professional assessment.

        USER DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        ASSESSMENT CRITERIA:
        1. Career stage (early, mid, senior)
        2. Growth potential
        3. Interest diversity

        Return a JSON analysis with these fields.
        """

    def get_insights_prompt(self, form_data, analysis):
        """Customize system prompt for personal profile insights."""
        return f"""
        Generate personalized career and personal development insights.

        USER DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        ANALYSIS:
        ```json
        {json.dumps(analysis, indent=2)}
        ```

        Generate 3-5 personalized insights and recommendations.
        Each insight should be a complete sentence or short paragraph.
        Make them specific to the user's profile, age, interests, and goals.
        """

    def get_default_analysis_result(self, form_data, error_message):
        """Custom default analysis for simple form."""
        return {"error": error_message}

async def main():
    # Create provider
    provider = OpenRouterProvider(
        api_key=API_KEY,
        model_name="openai/gpt-4o-mini"
    )

    # Create analytics
    analytics = SimpleAnalytics(provider=provider, verbose=True)

    # Create form processor
    processor = FormProcessor(
        form_class=SimpleForm,
        analytics_tools=analytics,
        openrouter_api_key=API_KEY,
        verbose=True
    )

    # Initialize session
    session_id, first_question = await processor.initialize()
    print(f"\nSession: {session_id}")
    print(f"Assistant: {first_question}")

    # Simulate a conversation
    messages = [
        "My name is John Smith and I'm 32 years old",
        "I work as a software engineer at a tech startup",
        "I enjoy hiking, coding, and playing chess in my free time",
        "My goal is to become a senior developer and eventually start my own company",
        "Can you analyze my profile?"
    ]

    for message in messages:
        print(f"\nUser: {message}")
        result = await processor.process_message(message, session_id)
        print(f"Assistant: {result.message}")
        print(f"Progress: {result.progress}%")

    # Get final form state
    state = await processor.get_form_state(session_id)
    print("\nFinal form data:")
    print(state.form)

if __name__ == "__main__":
    asyncio.run(main())
