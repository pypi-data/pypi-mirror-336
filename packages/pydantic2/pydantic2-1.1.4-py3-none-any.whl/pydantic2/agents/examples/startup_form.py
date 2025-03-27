#!/usr/bin/env python
"""
Startup form example with nested data structures.
"""

import os
import asyncio
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import json

# Import from our library
from pydantic2.agents import FormProcessor
from pydantic2.agents import BaseAnalyticsTools, OpenRouterProvider

# Get API key from environment
API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("Please set the OPENROUTER_API_KEY environment variable")

# Define nested models
class Founder(BaseModel):
    """Founder information model."""
    name: str = Field(default="", description="Founder's full name")
    role: str = Field(default="", description="Founder's role in the company")
    experience: str = Field(default="", description="Relevant experience and background")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile URL")

class Competitor(BaseModel):
    """Competitor information model."""
    name: str = Field(default="", description="Competitor company name")
    strengths: List[str] = Field(default_factory=list, description="Competitor's strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Competitor's weaknesses")

class FinancialData(BaseModel):
    """Financial information model."""
    revenue_model: str = Field(default="", description="How the company generates revenue")
    current_runway: str = Field(default="", description="Current financial runway")
    funding_stage: str = Field(default="", description="Current funding stage")
    funding_raised: float = Field(default=0.0, description="Total funding raised in USD")

class StartupForm(BaseModel):
    """Comprehensive startup information form with nested data."""
    company_name: str = Field(default="", description="Company name")
    tagline: str = Field(default="", description="Short company description/tagline")

    # Nested fields
    founders: List[Founder] = Field(default_factory=list, description="Information about company founders")
    competitors: List[Competitor] = Field(default_factory=list, description="Information about key competitors")
    financials: FinancialData = Field(default_factory=FinancialData, description="Financial information")

    # Other fields
    target_market: str = Field(default="", description="Description of the target market")
    problem_statement: str = Field(default="", description="Problem the company is solving")
    solution: str = Field(default="", description="Solution offered by the company")
    traction: List[str] = Field(default_factory=list, description="Current traction metrics and milestones")

# Startup analytics implementation
class StartupAnalytics(BaseAnalyticsTools):
    def get_analysis_prompt(self, form_data, form_schema):
        """Customize system prompt for startup analysis."""
        return f"""
        Analyze this startup data and provide a comprehensive assessment.

        STARTUP DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        Generate a detailed analysis with the following components:
        1. Market opportunity assessment
        2. Competitive positioning
        3. Team strength evaluation
        4. Financial viability
        5. Investment readiness score (0-100)

        Return your analysis as a structured JSON object with these fields.
        """

    def get_insights_prompt(self, form_data, analysis):
        """Customize system prompt for startup insights."""
        return f"""
        Generate strategic recommendations for this startup based on the analysis.

        STARTUP DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        ANALYSIS:
        ```json
        {json.dumps(analysis, indent=2)}
        ```

        Generate 5 strategic recommendations covering:
        - Market strategy
        - Competitive advantage
        - Team development
        - Financial strategy
        - Growth opportunities

        Each recommendation should be specific, actionable, and directly tied to the analysis.
        """

    def get_default_analysis_result(self, form_data, error_message):
        """Custom default analysis for startups."""
        return {
            "error": error_message,
            "market_opportunity": "Unable to analyze",
            "competitive_positioning": "Unable to analyze",
            "team_strength": "Unable to analyze",
            "financial_viability": "Unable to analyze",
            "investment_readiness": 0
        }

async def main():
    # Create provider
    provider = OpenRouterProvider(
        api_key=API_KEY,
        model_name="openai/gpt-4o-mini"
    )

    # Create analytics
    analytics = StartupAnalytics(provider=provider, verbose=True)

    # Create form processor
    processor = FormProcessor(
        form_class=StartupForm,
        analytics_tools=analytics,
        openrouter_api_key=API_KEY,
        verbose=True
    )

    # Initialize session
    session_id, first_question = await processor.initialize()
    print(f"\nSession: {session_id}")
    print(f"Assistant: {first_question}")

    # Simulate a conversation with complex nested data
    messages = [
        "Our startup is called EcoTrack and our tagline is 'Sustainability metrics for the modern enterprise'",

        "We have two founders: Sarah Johnson who is the CEO with 10 years of experience in enterprise software " +
        "and Michael Chen, our CTO who previously built machine learning systems at Google",

        "Our main competitors are CarbonAnalytics and GreenMetrics. CarbonAnalytics has strong enterprise relationships " +
        "but their product is outdated. GreenMetrics has a modern interface but lacks depth in data analytics.",

        "We're solving the problem that companies struggle to measure and report their environmental impact accurately. " +
        "Our solution is an AI-powered platform that automates data collection and generates regulatory compliance reports.",

        "Our target market is mid to large enterprises in manufacturing and logistics that need to comply with " +
        "environmental regulations. We've already onboarded 5 pilot customers and have an LOI from a Fortune 500 company.",

        "Our financial model is SaaS with tiered pricing. We've raised $1.2M in seed funding and have a runway of 18 months. " +
        "We're currently at the seed stage and planning for Series A in about 12 months.",

        "Can you analyze our startup and provide strategic recommendations?"
    ]

    for message in messages:
        print(f"\nUser: {message}")
        result = await processor.process_message(message, session_id)
        print(f"Assistant: {result.message}")
        print(f"Progress: {result.progress}%")

    # Get final form state
    state = await processor.get_form_state(session_id)
    print("\nFinal form data:")
    print(json.dumps(state.form, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
