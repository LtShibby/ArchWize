from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class DiagramRequest(BaseModel):
    """Model for receiving diagram generation requests"""
    prompt: str = Field(..., description="User's text description of the diagram they want to generate")
    diagram_type: Optional[str] = Field(None, description="Optional specific diagram type (flowchart, sequence, class, etc.)")
    theme: Optional[str] = Field(None, description="Optional theme for the diagram (default, forest, dark, etc.)")

class DiagramResponse(BaseModel):
    """Model for diagram generation responses"""
    mermaid_code: str = Field(..., description="Generated Mermaid.js syntax for the diagram")
    diagram_type: Optional[str] = Field(None, description="Type of diagram that was generated")
    generated_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the diagram was generated")

class ErrorResponse(BaseModel):
    """Model for error responses"""
    detail: str = Field(..., description="Error message")
    code: int = Field(..., description="Error code")
    
class User(BaseModel):
    """User model for future authentication implementation"""
    id: str
    email: str
    name: Optional[str] = None
    created_at: datetime
    diagrams_generated: int = 0