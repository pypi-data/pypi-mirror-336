from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class FormResult(BaseModel):
    """Result of form processing containing updated data and response."""
    message: str = Field(..., description="Response message to the user")
    form_update: Dict[str, Any] = Field(..., description="Updated form data")
    progress: int = Field(..., description="Current completion progress (0-100)")
    next_question: str = Field(..., description="Next question to ask")
    user_language: str = Field(default="en", description="Detected user language")
    insights: Optional[List[str]] = Field(default=None, description="Analysis insights if available")
    completion_achieved: bool = Field(default=False, description="Whether form completion has been achieved")
