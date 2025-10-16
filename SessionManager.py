from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid


class ConversationMessage(BaseModel):
    "Individual conversation Message"
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class CodeSubmission(BaseModel):
    "Code Submission Snapshot"
    code: str
    language: str
    timestamp: datetime = Field(default_factory=datetime.now)
    line_count: int = 0

class InterviewSession(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    language: str
    company: str
    start_time: datetime = Field(default_factory=datetime.now)
    end_time : Optional[datetime] = None

    #Problem details
    problem_id: Optional[str] = None
    problem_statement: Optional[str] = None
    problem_title : Optional[str] = None
    problem_hints : Optional[str] = None
    problem_topics : Optional[str] = None
    problem_difficulty : Optional[str] = None

    #Interview State

    current_state: str = "Introduction"
    is_active: bool = True

    #Interview Data

    conversation_history: list[ConversationMessage] = Field(default_factory=list)
    code_submissions: list[CodeSubmission] = Field(default_factory=list)

class SessionManager:

    """ Manages all interview Session"""

    def __init__(self):
        self._sessions: dict[str, InterviewSession] = {}

    #CRUD OPERATIONS
    
    def create_session(self, user_id : Optional[str] , 
    language: str = "Python", company: str = "Generic") -> InterviewSession:
        session_id = uuid.uuid4()
        session = InterviewSession(
            session_id = session_id,
            user_id=user_id,
            language=language,
            company = company
        )
        self._sessions[session_id] = session
        
        return session
    
    def get_session(self, session_id):
        return self._sessions[session_id]

    def update_session(self, session_id:str, **updates) -> bool:
        session = self._sessions[session_id]
        if not session:
            return False
        updated_data = session.model_dump()
        updated_data.update(updates)
        self._sessions[session_id] = InterviewSession(**updated_data)
        return True
    
    #Progress Tracking

    def set_problem(self, 
    session_id:str,
    problem_id:str,
    problem_statement: str,
    problem_title: str, 
    problem_hints: Optional[str],
    problem_topics: Optional[str],
    problem_difficulty: str) -> bool:

        session = self._sessions[session_id]

        updates = {
            "problem_id":problem_id,
            "problem_statement":problem_statement,
            "problem_title":problem_title,
            "problem_hints":problem_hints,
            "problem_topics":problem_topics,
            "problem_difficulty":problem_difficulty
        }
        return self.update_session(session_id, **updates)


#Conversation storage

def add_conversation_message(self, session_id: str, role: str, content: str) -> bool:
    "Add a message to conversation history"
    session = self._sessions[session_id]

    if not session:
        return False
    message = ConversationMessage(role=role, content=content)
    session.conversation_history.append(message)
    return True

def add_code_submission(self, session_id: str, 
code: str, language: str) -> bool:
    
    session = self._sessions[session_id]
    if not session:
        return False
    code = CodeSubmission(code=code, language=language)

    session.code_submissions.append(code)
    return True