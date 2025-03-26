from pydantic import BaseModel, Field, ConfigDict
from typing import TypeVar, Generic, Optional
from drf_pydantic import BaseModel as DRFBaseModel


class TestAgentResponse(BaseModel):
    """Response from test agent"""
    response: str = Field(description="Agent's response text")


class FormSettings(DRFBaseModel):
    """State for tracking form settings"""
    # Form data and progress
    progress: int = Field(default=0, description="Form progress (0-100)")
    prev_question: Optional[str] = Field(default=None, description="Previous question asked")
    prev_answer: Optional[str] = Field(default=None, description="Previous answer received")

    # Processing state
    feedback: Optional[str] = Field(default=None, description="Feedback on provided info")
    confidence: float = Field(
        default=0.0,
        ge=0, le=1,
        description="Confidence in state"
    )
    next_question: Optional[str] = Field(default=None, description="Next question to ask")
    next_question_explanation: Optional[str] = Field(
        default=None,
        description="Explanation of next question based on state"
    )
    user_language: Optional[str] = Field(default="", description="User's language (iso639-1)")


FormT = TypeVar('FormT', bound=BaseModel)


class FormState(BaseModel, Generic[FormT]):
    """Base state for tracking form progress and processing"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Form data and progress
    form: FormT
    settings: FormSettings = Field(default_factory=FormSettings)
