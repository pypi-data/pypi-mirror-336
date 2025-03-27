import uuid
from typing import Type, Dict, Any, Optional, List, Union, Tuple
from pydantic import BaseModel

from ..models.state import FormState, Settings
from ..models.results import FormResult
from ..tools.form_tools import FormTools
from ..tools.analytics_base import BaseAnalyticsTools
from ..core.session_manager import SessionManager, DB_PATH
from ..core.orchestrator import Orchestrator
from ..providers.openrouter import OpenRouterProvider
from ..utils.schema_utils import schema_to_model

class FormProcessor:
    """
    Main entry point for form processing.
    Manages session handling, data extraction, and form analytics.
    """

    def __init__(
        self,
        form_class: Union[Type[BaseModel], Dict[str, Any]],
        analytics_tools: Optional[BaseAnalyticsTools] = None,
        openrouter_api_key: Optional[str] = None,
        model: str = "openai/gpt-4o-mini",
        db_path: str = DB_PATH,
        client_id: str = "default",
        verbose: bool = False
    ):
        """
        Initialize form processor.

        Args:
            form_class: Form class or JSON schema
            analytics_tools: Analytics tools for completed forms
            openrouter_api_key: OpenRouter API key
            model: Model name for LLM
            db_path: Path to session database
            client_id: Client identifier
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self.api_key = openrouter_api_key
        self.client_id = client_id

        # Convert JSON schema to model if needed
        if isinstance(form_class, dict):
            if self.verbose:
                print("Converting JSON schema to Pydantic model")
            self.form_class = schema_to_model(form_class)
        else:
            self.form_class = form_class

        # Create LLM provider
        if not openrouter_api_key:
            raise ValueError("OpenRouter API key is required")

        self.provider = OpenRouterProvider(
            api_key=openrouter_api_key,
            model_name=model
        )

        # Create form tools
        self.form_tools = FormTools(
            provider=self.provider,
            verbose=verbose
        )

        # Initialize session manager
        self.session_manager = SessionManager(
            db_path=db_path,
            verbose=verbose
        )

        # Initialize orchestrator
        self.orchestrator = Orchestrator(
            form_tools=self.form_tools,
            analytics_tools=analytics_tools,
            verbose=verbose
        )

    async def initialize(
        self,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        initial_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, str]:
        """
        Initialize a new session or restore an existing one.

        Args:
            user_id: User identifier (generated if None)
            session_id: Session identifier for restoration
            initial_data: Initial form data

        Returns:
            Session ID and initial/current question
        """
        # Generate user ID if not provided
        if user_id is None:
            user_id = str(uuid.uuid4())

        # Handle session restoration
        if session_id:
            # Restore existing session
            self.session_manager.session_id = session_id
            state_dict = await self.session_manager.get_latest_state(session_id)

            if not state_dict:
                raise ValueError(f"Session {session_id} not found or has no state")

            # Extract settings and next question
            settings = state_dict.get("settings", {})
            next_question = settings.get("next_question", "Let's continue filling out the form.")

            return session_id, next_question
        else:
            # Create new session
            form_data = initial_data or {}
            form_class_name = self.form_class.__name__

            # Create session
            session_id = await self.session_manager.create_session(
                user_id=user_id,
                client_id=self.client_id,
                form_class=form_class_name
            )

            # Create initial form instance
            form_instance = self.form_class(**form_data)

            # Default initial question
            next_question = "Please tell me about yourself so we can fill out the form."

            # Create initial state
            initial_state = FormState(
                form=form_instance.model_dump(),
                settings=Settings(next_question=next_question)
            )

            # Save initial state
            await self.session_manager.save_state(initial_state.model_dump(), session_id)

            return session_id, next_question

    async def process_message(
        self,
        message: str,
        session_id: str
    ) -> FormResult:
        """
        Process a user message and update form state.

        Args:
            message: User message
            session_id: Session identifier

        Returns:
            Processing result
        """
        # Validate session
        if not session_id:
            raise ValueError("Session ID is required")

        # Set current session
        self.session_manager.session_id = session_id

        # Get latest state
        state_dict = await self.session_manager.get_latest_state(session_id)
        if not state_dict:
            raise ValueError(f"No state found for session {session_id}")

        # Get session info
        session_info = await self.session_manager.get_session(session_id)
        user_id = session_info.get("user_id", "")

        # Reconstruct form state
        form_data = state_dict.get("form", {})
        settings_data = state_dict.get("settings", {})
        settings = Settings(**settings_data)

        if self.verbose:
            print(f"[FormProcessor] Processing message: '{message}'")
            print(f"[FormProcessor] Current form data: {form_data}")

        # Create form instance
        form_instance = self.form_class(**form_data)
        form_state = FormState(form=form_instance, settings=settings)

        # Get message history
        message_history = await self.session_manager.get_messages(session_id)

        # Save user message
        await self.session_manager.save_message("user", message, session_id)

        # Process message with orchestrator
        result = await self.orchestrator.process(
            message=message,
            form_state=form_state,
            form_class=self.form_class,
            session_id=session_id,
            user_id=user_id,
            message_history=message_history
        )

        # Save assistant message
        await self.session_manager.save_message("assistant", result.message, session_id)

        # Log form update results
        if self.verbose:
            print(f"[FormProcessor] Form update after processing: {result.form_update}")

        # Update form with the results and create a new form instance
        form_result_instance = self.form_class(**result.form_update)

        # Update and save form state
        updated_state = FormState(
            form=form_result_instance,
            settings=Settings(
                progress=result.progress,
                next_question=result.next_question,
                prev_question=settings.next_question,
                prev_answer=message,
                language=result.user_language
            )
        )

        # Save updated state - need to convert to dict for storage
        state_to_save = updated_state.model_dump()

        if self.verbose:
            print(f"[FormProcessor] Saving state to session {session_id}:")
            print(f"[FormProcessor] - form: {state_to_save.get('form', {})}")
            print(f"[FormProcessor] - settings: {state_to_save.get('settings', {})}")

        await self.session_manager.save_state(state_to_save, session_id)

        return result

    async def get_form_state(self, session_id: Optional[str] = None) -> FormState:
        """
        Get current form state.

        Args:
            session_id: Session identifier (if None, use current session)

        Returns:
            Current form state with form property as a Pydantic model instance
        """
        sid = session_id or self.session_manager.session_id
        if not sid:
            raise ValueError("No active session")

        state_dict = await self.session_manager.get_latest_state(sid)
        if not state_dict:
            raise ValueError(f"No state found for session {sid}")

        form_data = state_dict.get("form", {})
        settings_data = state_dict.get("settings", {})

        if self.verbose:
            print(f"[FormProcessor.get_form_state] Retrieved state for session {sid}:")
            print(f"[FormProcessor.get_form_state] - form: {form_data}")
            print(f"[FormProcessor.get_form_state] - settings: {settings_data}")

        # Convert form_data to Pydantic model instance instead of keeping as dict
        form_instance = self.form_class(**form_data)

        form_state = FormState(
            form=form_instance,  # Now form is a Pydantic model instance, not a dict
            settings=Settings(**settings_data)
        )

        if self.verbose:
            print(f"[FormProcessor.get_form_state] Returning FormState with form: {form_instance}")

        return form_state

    async def get_session_history(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get complete session history.

        Args:
            session_id: Session identifier (if None, use current session)

        Returns:
            Session history details
        """
        sid = session_id or self.session_manager.session_id
        if not sid:
            raise ValueError("No active session")

        # Get session info
        session_info = await self.session_manager.get_session(sid)

        # Get messages
        messages = await self.session_manager.get_messages(sid, limit=1000)

        # Get states
        states = await self.session_manager.get_state_history(sid)

        return {
            "session": session_info,
            "messages": messages,
            "states": states
        }
