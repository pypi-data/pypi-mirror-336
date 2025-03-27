from typing import Dict, Any, Optional, Union, TypeVar, Generic
from pydantic import BaseModel, Field
from drf_pydantic import BaseModel as DRFBaseModel

# Generic type for form models
FormModel = TypeVar('FormModel', bound=BaseModel)

class Settings(DRFBaseModel):
    """Form processing settings and state tracking."""
    progress: int = Field(default=0, description="Completion progress (0-100)")
    next_question: str = Field(default="", description="Next question to ask")
    prev_question: str = Field(default="", description="Previous question asked")
    prev_answer: str = Field(default="", description="Last user answer")
    language: str = Field(default="en", description="User's detected language")

class FormState(BaseModel):
    """Complete form state containing form data and processing settings."""
    form: Union[Dict[str, Any], BaseModel] = Field(
        default_factory=dict,
        description="Current form data (either dict or Pydantic model)"
    )
    settings: Settings = Field(default_factory=Settings, description="Processing settings")

    def is_complete(self) -> bool:
        """Check if the form is complete."""
        return self.settings.progress >= 100

    def get_form_json(self) -> Dict[str, Any]:
        """Get form data as a JSON-serializable dict."""
        if isinstance(self.form, dict):
            return self.form
        elif isinstance(self.form, BaseModel):
            return self.form.model_dump()
        return {}

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """
        Override model_dump to handle Pydantic instances in form field.
        This ensures correct serialization when the form field contains a Pydantic model.
        """
        # Create a copy of self without modifying the original
        data = super().model_dump(**kwargs)

        # If form is a Pydantic model, convert it to dict
        if isinstance(self.form, BaseModel):
            data["form"] = self.form.model_dump(**kwargs)

        return data
