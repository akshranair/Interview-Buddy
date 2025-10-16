from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


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
    