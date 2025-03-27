import os
import asyncio
import json
from typing import Dict, List, Optional, Union, Literal
from uuid import uuid4
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from pydantic2.agents.providers.openrouter import OpenRouterProvider
from pydantic2.agents.core.form_processor import FormProcessor
from pydantic2.agents.tools.analytics_base import BaseAnalyticsTools
from pydantic2.agents.utils.model_factory import UniversalModelFactory

# Примеры вспомогательных функций для создания экземпляров с дефолтными значениями
def default_personal_info():
    return PersonalInfo(full_name="", age=0, email="")

def default_professional_info():
    return ProfessionalInfo(
        employment_status=EmploymentStatus.UNEMPLOYED,
        education_level=EducationLevel.HIGH_SCHOOL
    )

def default_product_usage():
    return ProductUsage(uses_product=False)

# Define our questionnaire models
class PersonalInfo(BaseModel):
    full_name: str = Field(description="Full name of the respondent", default="")
    age: int = Field(description="Age of the respondent in years", default=0)
    email: str = Field(description="Email address for contact", default="")
    phone: Optional[str] = Field(None, description="Phone number (optional)")

class EmploymentStatus(str, Enum):
    """Employment status of the respondent"""
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    SELF_EMPLOYED = "Self-employed"
    STUDENT = "Student"
    UNEMPLOYED = "Unemployed"
    RETIRED = "Retired"

class EducationLevel(str, Enum):
    """Highest level of education completed"""
    HIGH_SCHOOL = "High School"
    ASSOCIATE = "Associate's Degree"
    BACHELOR = "Bachelor's Degree"
    MASTER = "Master's Degree"
    DOCTORATE = "Doctorate"
    OTHER = "Other"

class SatisfactionRating(int, Enum):
    """Satisfaction rating from 1 (very dissatisfied) to 5 (very satisfied)"""
    VERY_DISSATISFIED = 1
    DISSATISFIED = 2
    NEUTRAL = 3
    SATISFIED = 4
    VERY_SATISFIED = 5

class ProfessionalInfo(BaseModel):
    employment_status: EmploymentStatus = Field(description="Current employment status", default=EmploymentStatus.UNEMPLOYED)
    job_title: Optional[str] = Field(None, description="Current job title, if employed")
    years_experience: Optional[int] = Field(None, description="Years of work experience in their field")
    education_level: EducationLevel = Field(description="Highest level of education completed", default=EducationLevel.HIGH_SCHOOL)

class ProductUsage(BaseModel):
    uses_product: bool = Field(description="Whether the respondent uses our product", default=False)
    usage_frequency: Optional[str] = Field(None, description="How often they use our product (e.g., daily, weekly)")
    favorite_features: Optional[List[str]] = Field(None, description="List of favorite features")
    satisfaction_rating: Optional[SatisfactionRating] = Field(None, description="Satisfaction rating from 1-5")

class FeedbackInfo(BaseModel):
    improvement_suggestions: Optional[str] = Field(None, description="Suggestions for product improvement")
    pain_points: Optional[List[str]] = Field(None, description="Pain points or issues with the product")
    would_recommend: Optional[bool] = Field(None, description="Whether they would recommend the product to others")
    additional_comments: Optional[str] = Field(None, description="Any additional comments or feedback")

class SurveyQuestionnaire(BaseModel):
    """A comprehensive survey questionnaire with multiple sections"""
    personal_info: PersonalInfo = Field(description="Basic personal information", default_factory=default_personal_info)
    professional_info: ProfessionalInfo = Field(description="Professional background information", default_factory=default_professional_info)
    product_usage: ProductUsage = Field(description="Information about product usage", default_factory=default_product_usage)
    feedback: Optional[FeedbackInfo] = Field(None, description="Feedback and improvement suggestions")


# Define analytics tools for the questionnaire
class QuestionnaireAnalytics(BaseAnalyticsTools):
    """Analytics tools for analyzing questionnaire responses"""

    async def analyze_form(self, form_data, form_schema):
        """Alias method to analyze_responses for compatibility with base class"""
        form_data_obj = SurveyQuestionnaire.model_validate(form_data)
        return await self.analyze_responses(form_data_obj)

    async def analyze_responses(self, form_data: SurveyQuestionnaire) -> Dict:
        """Analyze the questionnaire responses and provide insights"""
        insights = {
            "completion_rate": self._calculate_completion_rate(form_data),
            "satisfaction_score": self._get_satisfaction_score(form_data),
            "demographic_segment": self._determine_demographic_segment(form_data),
            "improvement_areas": self._extract_improvement_areas(form_data),
            "recommendation_likelihood": self._calculate_recommendation_likelihood(form_data),
        }
        return insights

    def _calculate_completion_rate(self, form_data: SurveyQuestionnaire) -> float:
        """Calculate the completion rate of the questionnaire"""
        total_fields = 14  # Total possible fields across all sections
        filled_fields = 0

        # Count filled personal info fields
        for field in form_data.personal_info.model_fields_set:
            if getattr(form_data.personal_info, field) is not None:
                filled_fields += 1

        # Count filled professional info fields
        for field in form_data.professional_info.model_fields_set:
            if getattr(form_data.professional_info, field) is not None:
                filled_fields += 1

        # Count filled product usage fields
        for field in form_data.product_usage.model_fields_set:
            if getattr(form_data.product_usage, field) is not None:
                filled_fields += 1

        # Count filled feedback fields if feedback exists
        if form_data.feedback:
            for field in form_data.feedback.model_fields_set:
                if getattr(form_data.feedback, field) is not None:
                    filled_fields += 1

        return round(filled_fields / total_fields * 100, 2)

    def _get_satisfaction_score(self, form_data: SurveyQuestionnaire) -> Optional[int]:
        """Get the satisfaction score if available"""
        if form_data.product_usage.satisfaction_rating:
            return form_data.product_usage.satisfaction_rating.value
        return None

    def _determine_demographic_segment(self, form_data: SurveyQuestionnaire) -> str:
        """Determine the demographic segment of the respondent"""
        age = form_data.personal_info.age
        employment = form_data.professional_info.employment_status
        education = form_data.professional_info.education_level

        if age < 25:
            if education in [EducationLevel.BACHELOR, EducationLevel.MASTER, EducationLevel.DOCTORATE]:
                return "Young Professional"
            else:
                return "Student/Early Career"
        elif 25 <= age < 40:
            if employment in [EmploymentStatus.FULL_TIME, EmploymentStatus.SELF_EMPLOYED]:
                return "Mid-Career Professional"
            else:
                return "Transitioning Professional"
        elif 40 <= age < 60:
            return "Established Professional"
        else:
            if employment == EmploymentStatus.RETIRED:
                return "Retiree"
            else:
                return "Senior Professional"

    def _extract_improvement_areas(self, form_data: SurveyQuestionnaire) -> List[str]:
        """Extract improvement areas from feedback"""
        areas = []

        if form_data.feedback and form_data.feedback.pain_points:
            areas.extend(form_data.feedback.pain_points)

        if form_data.feedback and form_data.feedback.improvement_suggestions:
            # Add generic improvement area based on suggestion
            areas.append("Product Enhancement Needed")

        if form_data.product_usage.satisfaction_rating:
            if form_data.product_usage.satisfaction_rating.value < 3:
                areas.append("General Satisfaction Issues")

        return areas if areas else ["No specific improvement areas identified"]

    def _calculate_recommendation_likelihood(self, form_data: SurveyQuestionnaire) -> str:
        """Calculate the likelihood of recommending the product"""
        if form_data.feedback and form_data.feedback.would_recommend is not None:
            return "High" if form_data.feedback.would_recommend else "Low"

        if form_data.product_usage.satisfaction_rating:
            if form_data.product_usage.satisfaction_rating.value >= 4:
                return "Likely"
            elif form_data.product_usage.satisfaction_rating.value == 3:
                return "Neutral"
            else:
                return "Unlikely"

        return "Unknown"

    def get_insights_prompt(self, form_data, analysis):
        """Customize system prompt for questionnaire insights."""
        return f"""
        Generate personalized recommendations based on this survey analysis.

        SURVEY DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        ANALYSIS:
        ```json
        {json.dumps(analysis, indent=2)}
        ```

        Generate 3-5 personalized recommendations for the respondent.
        Each recommendation should be specific to their demographic segment,
        satisfaction level, and feedback provided.

        Focus on addressing any improvement areas identified and enhancing their experience.
        """


# Main function to run the questionnaire
async def main():
    # Initialize provider
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("Warning: OPENROUTER_API_KEY environment variable not set.")
        api_key = "your_openrouter_api_key_here"  # For demonstration purposes only

    analytics = QuestionnaireAnalytics(provider=OpenRouterProvider(api_key=api_key))

    # Display menu
    print("=" * 50)
    print("  SURVEY QUESTIONNAIRE SYSTEM")
    print("=" * 50)
    print("1. Start a new survey")
    print("2. Continue existing survey")
    print("=" * 50)

    choice = input("Enter your choice (1 or 2): ")

    session_id = None
    user_id = f"user_{uuid4()}"  # Generate a user ID

    # Create form processor - use database from settings
    form_processor = FormProcessor(
        form_class=SurveyQuestionnaire,
        analytics_tools=analytics,
        openrouter_api_key=api_key,
        client_id="questionnaire",
        verbose=True
    )

    # Initialize session
    if choice == "1":
        # New session - create with default values
        empty_form = SurveyQuestionnaire()
        initial_data = empty_form.model_dump()
        session_id, welcome_msg = await form_processor.initialize(
            user_id=user_id,
            initial_data=initial_data
        )
        print(f"Created new session with ID: {session_id}")
    else:
        # Existing session
        session_id = input("Enter your session ID: ")
        try:
            session_id, welcome_msg = await form_processor.initialize(
                user_id=user_id,
                session_id=session_id
            )
            print(f"Continuing session {session_id}...")
        except ValueError as e:
            print(f"Error: {e}")
            return

    # Simulate a conversation
    async def process_message(message: str):
        response = await form_processor.process_message(message, session_id)
        print(f"\nAssistant: {response}")

        # Display form progress
        try:
            form_state = await form_processor.get_form_state(session_id)
            progress = form_state.settings.progress or 0
            print(f"Progress: {progress}%")
        except Exception as e:
            print(f"Error getting form state: {e}")

    # Welcome message for different scenarios
    if choice == "1":
        # Display the welcome message for a new survey
        await process_message("Hello! I'm here to conduct a survey about our product. Can we start with your name, age, and email?")
    else:
        # For continuing a session, let's check the progress and ask an appropriate question
        await process_message("Welcome back to our survey! Let's continue where we left off.")

    # Interactive loop
    try:
        while True:
            user_input = input("\nYou (type 'exit' to quit): ")
            if user_input.lower() in ['exit', 'quit']:
                # Get final form state before exiting
                try:
                    form_state = await form_processor.get_form_state(session_id)
                    form_data = form_state.form
                    progress = form_state.settings.progress or 0

                    print(f"\nCurrent completion rate: {progress}%")

                    if progress >= 95:
                        print("\nThank you for completing the survey!")

                        # Display final form data
                        print("\nFinal Survey Data:")
                        print(json.dumps(form_data, indent=2))

                        # Generate insights if analytics are available
                        try:
                            form_model = SurveyQuestionnaire.model_validate(form_data)
                            insights = await analytics.analyze_responses(form_model)
                            print("\nSurvey Insights:")
                            print(json.dumps(insights, indent=2))
                        except Exception as e:
                            print(f"Error generating insights: {e}")
                    else:
                        print(f"\nSurvey saved. You can continue later with session ID: {session_id}")
                except Exception as e:
                    print(f"Error accessing form data: {e}")
                break

            await process_message(user_input)

    except KeyboardInterrupt:
        print(f"\nSurvey saved. You can continue later with session ID: {session_id}")

    # Generate random example data
    print("\nExample of randomly generated data:")
    factory = UniversalModelFactory(SurveyQuestionnaire)
    random_data = factory.build()
    print(random_data.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
