from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel, Field

class FormDependencies(BaseModel):
    """Dependencies container for form tools."""
    form_class: Type[BaseModel]
    form_data: Dict[str, Any] = Field(default_factory=dict)
    user_id: str = ""
    session_id: str = ""
    progress: int = 0
    message_history: List[Dict[str, Any]] = Field(default_factory=list)
    user_language: str = "en"
    verbose: bool = False
