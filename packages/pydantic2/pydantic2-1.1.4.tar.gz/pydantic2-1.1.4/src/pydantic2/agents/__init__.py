"""
Pydantic AI Form Processor - Simplified

A framework for intelligent, session-based form processing using LLMs.
"""

__version__ = "0.1.0"

# Core exports
from .core.form_processor import FormProcessor
from .tools.analytics_base import BaseAnalyticsTools
from .providers.openrouter import OpenRouterProvider
from .providers.base import ProviderBase

# Utils
from .utils.schema_utils import schema_to_model
from .utils.model_factory import UniversalModelFactory

# For type hints
from .models.state import FormState, Settings
from .models.results import FormResult
from .models.dependencies import FormDependencies
