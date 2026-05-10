from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Speaker(str, Enum):
    PROFESSOR = "professor"
    STUDENT = "student"
    UNKNOWN = "unknown"

class LectureChunk(BaseModel):
    # Identity
    chunk_id: str                     
    session_id: str                      
    session_number: int        
    session_label: str         
    session_date: Optional[str] = None   

    # Content
    text: str                            #transcribed text
    speaker: Speaker = Speaker.UNKNOWN

    # Temporal
    start_time: float                    
    end_time: float                      
    timestamp_label: str                 

    # Topic tagging (LLM-assigned during ingestion)
    topic: Optional[str] = None          
    keywords: list[str] = Field(default_factory=list)

    # Source
    video_url: Optional[str] = None      # YouTube URL
    video_title: Optional[str] = None


class Session(BaseModel):
    """One lecture / meeting session."""
    session_id: str
    session_number: int
    title: str
    video_url: Optional[str] = None
    duration_seconds: float
    chunk_count: int = 0


class SourceCitation(BaseModel):
    chunk_id: str
    session_id: str
    session_number: int
    timestamp_label: str
    video_url: Optional[str] = None
    timestamp_seconds: float             
    excerpt: str                      


class QueryResult(BaseModel):
    answer: str
    sources: list[SourceCitation]
    contradiction_found: bool = False
    contradiction_explanation: Optional[str] = None


class ConceptTimelineEntry(BaseModel):
    session_number: int
    session_id: str
    timestamp_label: str
    timestamp_seconds: float
    summary: str                    
    video_url: Optional[str] = None
