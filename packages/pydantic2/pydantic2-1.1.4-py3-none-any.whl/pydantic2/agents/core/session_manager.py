import json
import datetime
import uuid
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
import peewee as pw

# Путь к директории db относительно текущего файла (core/session_manager.py -> core -> agents17 -> pydantic2 -> db)
CURRENT_DIR = Path(__file__).parent  # core/src
MODULE_DIR = CURRENT_DIR.parent.parent  # pydantic2
DB_DIR = MODULE_DIR / "db"
DB_DIR.mkdir(exist_ok=True)  # Создаем директорию, если она отсутствует
DB_PATH = DB_DIR / "sessions.db"

# Database setup
db = pw.SqliteDatabase(None)  # Инициализируем без пути

class BaseModel(pw.Model):
    class Meta:
        database = db

class Session(BaseModel):
    session_id = pw.CharField(primary_key=True)
    user_id = pw.CharField()
    client_id = pw.CharField()
    form_class = pw.CharField()
    created_at = pw.DateTimeField(default=datetime.datetime.now)

class State(BaseModel):
    id = pw.AutoField()
    session = pw.ForeignKeyField(Session, backref='states')
    data = pw.TextField()  # JSON data
    created_at = pw.DateTimeField(default=datetime.datetime.now)

class Message(BaseModel):
    id = pw.AutoField()
    session = pw.ForeignKeyField(Session, backref='messages')
    role = pw.CharField()  # 'user' or 'assistant'
    content = pw.TextField()
    created_at = pw.DateTimeField(default=datetime.datetime.now)

class SessionManager:
    """Session manager for form processing."""

    def __init__(self, db_path: str = DB_PATH, verbose: bool = False):
        """Initialize session manager."""
        self.db_path = db_path
        self.verbose = verbose
        self.session_id = None
        self._setup_database()

    def _setup_database(self):
        """Setup the database connection and create tables if needed."""
        try:
            db.init(self.db_path)
            db.connect()
            db.create_tables([Session, State, Message])
        except Exception as e:
            if self.verbose:
                print(f"Database setup error: {e}")

    async def create_session(
        self,
        user_id: str,
        client_id: str = "default",
        form_class: str = "BaseForm"
    ) -> str:
        """
        Create a new session and return its ID.

        Args:
            user_id: User identifier
            client_id: Client identifier
            form_class: Form class name

        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())

        try:
            with db.atomic():
                Session.create(
                    session_id=session_id,
                    user_id=user_id,
                    client_id=client_id,
                    form_class=form_class
                )
            self.session_id = session_id
            return session_id
        except Exception as e:
            if self.verbose:
                print(f"Error creating session: {e}")
            return None

    async def get_session(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get session information.

        Args:
            session_id: Session ID (if None, use current session)

        Returns:
            Session information as dictionary
        """
        sid = session_id or self.session_id
        if not sid:
            return {}

        try:
            session = Session.get(Session.session_id == sid)
            return {
                "session_id": session.session_id,
                "user_id": session.user_id,
                "client_id": session.client_id,
                "form_class": session.form_class,
                "created_at": session.created_at.isoformat()
            }
        except Session.DoesNotExist:
            return {}
        except Exception as e:
            if self.verbose:
                print(f"Error getting session: {e}")
            return {}

    async def save_state(self, state_data: Dict[str, Any], session_id: Optional[str] = None) -> bool:
        """
        Save form state to the database.

        Args:
            state_data: Form state data (dict or object with model_dump method)
            session_id: Session ID (if None, use current session)

        Returns:
            Success flag
        """
        sid = session_id or self.session_id
        if not sid:
            return False

        # Ensure we have a serializable dict
        if not isinstance(state_data, dict):
            # Try to convert to dict if it has model_dump or dict method
            if hasattr(state_data, "model_dump"):
                state_data = state_data.model_dump()
            elif hasattr(state_data, "dict"):
                state_data = state_data.dict()
            else:
                if self.verbose:
                    print(f"Cannot serialize state data of type {type(state_data)}")
                return False

        try:
            session = Session.get(Session.session_id == sid)
            State.create(
                session=session,
                data=json.dumps(state_data)
            )
            return True
        except Exception as e:
            if self.verbose:
                print(f"Error saving state: {e}")
            return False

    async def get_latest_state(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the latest form state.

        Args:
            session_id: Session ID (if None, use current session)

        Returns:
            Latest form state
        """
        sid = session_id or self.session_id
        if not sid:
            return {}

        try:
            session = Session.get(Session.session_id == sid)
            state = (State
                    .select()
                    .where(State.session == session)
                    .order_by(State.created_at.desc())
                    .first())

            if state:
                return json.loads(state.data)
            return {}
        except Exception as e:
            if self.verbose:
                print(f"Error getting latest state: {e}")
            return {}

    async def save_message(
        self,
        role: str,
        content: str,
        session_id: Optional[str] = None
    ) -> bool:
        """
        Save a message to the database.

        Args:
            role: Message role ('user' or 'assistant')
            content: Message content
            session_id: Session ID (if None, use current session)

        Returns:
            Success flag
        """
        sid = session_id or self.session_id
        if not sid:
            return False

        try:
            session = Session.get(Session.session_id == sid)
            Message.create(
                session=session,
                role=role,
                content=content
            )
            return True
        except Exception as e:
            if self.verbose:
                print(f"Error saving message: {e}")
            return False

    async def get_messages(self, session_id: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get message history.

        Args:
            session_id: Session ID (if None, use current session)
            limit: Maximum number of messages to return

        Returns:
            Message history as list of dictionaries
        """
        sid = session_id or self.session_id
        if not sid:
            return []

        try:
            session = Session.get(Session.session_id == sid)
            messages = (Message
                       .select()
                       .where(Message.session == session)
                       .order_by(Message.created_at)
                       .limit(limit))

            return [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "created_at": msg.created_at.isoformat(),
                    "session_id": msg.session_id
                }
                for msg in messages
            ]
        except Exception as e:
            if self.verbose:
                print(f"Error getting messages: {e}")
            return []

    async def get_state_history(self, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get state history.

        Args:
            session_id: Session ID (if None, use current session)

        Returns:
            State history as list of dictionaries
        """
        sid = session_id or self.session_id
        if not sid:
            return []

        try:
            session = Session.get(Session.session_id == sid)
            states = (State
                     .select()
                     .where(State.session == session)
                     .order_by(State.created_at))

            return [
                {**json.loads(state.data), "created_at": state.created_at.isoformat()}
                for state in states
            ]
        except Exception as e:
            if self.verbose:
                print(f"Error getting state history: {e}")
            return []
