from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import json
import re
from ..providers.base import ProviderBase

class BaseAnalyticsTools(ABC):
    """
    Base class for analytics tools.
    These tools should only be used when form completion is 100%.
    """

    def __init__(self, provider: ProviderBase, verbose: bool = False):
        """
        Initialize analytics tools.

        Args:
            provider: LLM provider
            verbose: Enable verbose logging
        """
        self.provider = provider
        self.verbose = verbose

    async def analyze_form(
        self,
        form_data: Dict[str, Any],
        form_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze form data and generate analysis.

        Args:
            form_data: Completed form data
            form_schema: Form JSON schema

        Returns:
            Analysis results
        """
        # Get custom system prompt from child class
        system_prompt = self.get_analysis_prompt(form_data, form_schema)

        try:
            # Call LLM provider with response format as JSON
            result = await self.provider.invoke(
                system=system_prompt,
                user="",
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            # Extract content from response
            content = result.choices[0].message.content

            # Convert to dictionary if it's a string
            if isinstance(content, str):
                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    if self.verbose:
                        print(f"JSON decode error in analysis: {e}")
                    return self.get_default_analysis_result(form_data, str(e))

            return content
        except Exception as e:
            if self.verbose:
                print(f"Analysis error: {e}")
            return self.get_default_analysis_result(form_data, str(e))

    async def generate_insights(
        self,
        form_data: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> List[str]:
        """
        Generate insights based on form analysis.

        Args:
            form_data: Completed form data
            analysis: Analysis results from analyze_form

        Returns:
            List of insights
        """
        # Get custom system prompt from child class
        system_prompt = self.get_insights_prompt(form_data, analysis)

        try:
            # Call LLM provider
            result = await self.provider.invoke(
                system=system_prompt,
                user="",
                temperature=0.7
            )

            # Extract content from response
            content = result.choices[0].message.content

            # Process insights with helper method
            return self._process_insights(content)
        except Exception as e:
            if self.verbose:
                print(f"Insights error: {e}")
            return self.get_default_insights(str(e))

    def _process_insights(self, content: str) -> List[str]:
        """
        Process raw LLM output into formatted insights.

        Args:
            content: Raw LLM response

        Returns:
            List of formatted insights
        """
        # Split into individual insights (by line)
        insights = [line.strip() for line in content.split("\n") if line.strip()]

        # Clean up numbering and bullet points
        insights = [re.sub(r"^\d+\.\s*|\*\s+|-\s+", "", insight) for insight in insights]

        # Apply custom formatting if implemented by child class
        return self.format_insights(insights)

    def get_analysis_prompt(self, form_data: Dict[str, Any], form_schema: Dict[str, Any]) -> str:
        """
        Get the system prompt for analysis.
        Override this method in child classes for domain-specific prompts.

        Args:
            form_data: Form data to analyze
            form_schema: Form schema

        Returns:
            System prompt for LLM
        """
        return f"""
        Analyze this form data and generate a comprehensive assessment.

        FORM DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        FORM SCHEMA:
        ```json
        {json.dumps(form_schema, indent=2)}
        ```

        Provide a detailed analysis with relevant metrics and observations.
        Return your analysis as a structured JSON object.
        """

    def get_insights_prompt(self, form_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """
        Get the system prompt for insights generation.
        Override this method in child classes for domain-specific prompts.

        Args:
            form_data: Form data
            analysis: Analysis results

        Returns:
            System prompt for LLM
        """
        return f"""
        Generate actionable insights based on this analysis.

        FORM DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        ANALYSIS:
        ```json
        {json.dumps(analysis, indent=2)}
        ```

        Generate 3-5 specific, actionable insights based on the provided data and analysis.
        Each insight should be a complete sentence or short paragraph.
        Make them specific to the context of the form data.
        """

    def get_default_analysis_result(self, form_data: Dict[str, Any], error_message: str) -> Dict[str, Any]:
        """
        Get default analysis result for error handling.
        Override this method in child classes for domain-specific defaults.

        Args:
            form_data: Form data
            error_message: Error message

        Returns:
            Default analysis result
        """
        return {
            "error": error_message,
            "status": "error",
            "message": "Unable to analyze the form data"
        }

    def get_default_insights(self, error_message: str) -> List[str]:
        """
        Get default insights for error handling.
        Override this method in child classes for domain-specific defaults.

        Args:
            error_message: Error message

        Returns:
            Default insights
        """
        return ["Unable to generate insights due to an error."]

    def format_insights(self, insights: List[str]) -> List[str]:
        """
        Format the insights list.
        Override this method in child classes for custom formatting.

        Args:
            insights: Raw insights list

        Returns:
            Formatted insights list
        """
        return insights
