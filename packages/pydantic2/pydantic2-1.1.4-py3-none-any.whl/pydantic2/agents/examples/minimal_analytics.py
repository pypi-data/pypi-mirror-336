#!/usr/bin/env python
"""
Minimal example showing how to create custom analytics with BaseAnalyticsTools.
"""

import os
import asyncio
from typing import Dict, Any, List
import json

# Import from our library
from pydantic2.agents import BaseAnalyticsTools, OpenRouterProvider

# Create a minimal analytics class by only overriding the prompt methods
class MinimalAnalytics(BaseAnalyticsTools):
    """
    Minimal analytics implementation that only customizes the prompts.
    This demonstrates how easy it is to create a new analytics tool.
    """

    def get_analysis_prompt(self, form_data: Dict[str, Any], form_schema: Dict[str, Any]) -> str:
        """
        Customize the analysis prompt for your specific domain.

        This is all you need to define to create a basic analytics tool!
        """
        return f"""
        You are a data analyst specializing in user profile data.
        Analyze this user profile and provide insights.

        USER DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        Produce a brief analysis with these components:
        1. User demographic category (student, professional, retired, etc.)
        2. Main interests or skills
        3. Career stage assessment

        Return your analysis as a simple JSON object with these three fields.
        """

    def get_insights_prompt(self, form_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """
        Customize the insights prompt for your specific domain.

        This is all you need to define for basic insights generation!
        """
        return f"""
        Based on this user profile and analysis, generate helpful suggestions.

        USER DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        ANALYSIS:
        ```json
        {json.dumps(analysis, indent=2)}
        ```

        Provide 3 concise, personalized recommendations for this user.
        Make them actionable and specific to their profile.
        """


async def demo():
    """Run a demo of the minimal analytics."""
    api_key = os.environ.get("OPENROUTER_API_KEY", "dummy_key_for_demo")

    # Sample user data
    user_data = {
        "name": "Alex Chen",
        "age": 28,
        "occupation": "Software Developer",
        "skills": ["Python", "JavaScript", "Machine Learning"],
        "education": "Bachelor's in Computer Science",
        "goals": "Transition to a machine learning engineer role"
    }

    # Create provider
    provider = OpenRouterProvider(api_key=api_key)

    # Create minimal analytics (just 2 methods!)
    analytics = MinimalAnalytics(provider=provider, verbose=True)

    print("MINIMAL ANALYTICS DEMO")
    print("=" * 50)

    print("\nRunning analysis...")
    analysis = await analytics.analyze_form(user_data, {})
    print(f"Analysis result:\n{json.dumps(analysis, indent=2)}")

    print("\nGenerating insights...")
    insights = await analytics.generate_insights(user_data, analysis)

    print("\nInsights:")
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")

    print("\nDemo complete! Notice how we only needed to define 2 template methods.")


if __name__ == "__main__":
    asyncio.run(demo())
