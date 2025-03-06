from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from datetime import datetime
from enum import Enum
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from services import DiagramService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"api_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("archwize_api")

load_dotenv()

app = FastAPI(title="ArchWize API", description="AI-Powered Diagram & Architecture Flowchart Generator")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiagramOrientation(str, Enum):
    TOP_DOWN = "TD"
    LEFT_RIGHT = "LR"

class DiagramRequest(BaseModel):
    prompt: str
    orientation: DiagramOrientation = Field(default=DiagramOrientation.TOP_DOWN, description="Diagram orientation: TD (top-down) or LR (left-right)")

class DiagramResponse(BaseModel):
    mermaid_code: str
    success: bool = True
    message: str = "Diagram generated successfully"

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str = "Failed to generate diagram"

@app.get("/")
def home():
    logger.info("Home endpoint accessed")
    return {"message": "ArchWize Backend Running!"}

@app.post("/generate")
async def generate_diagram(request: DiagramRequest):
    logger.info(f"Received diagram generation request: {request.prompt} with orientation: {request.orientation}")
    try:
        # Use the DiagramService to generate the diagram with the specified orientation
        mermaid_code = await DiagramService.generate_mermaid_diagram(request.prompt, request.orientation)
        logger.info("Diagram generation successful")
        return DiagramResponse(mermaid_code=mermaid_code)
    except ValueError as e:
        # Specific handling for validation errors
        error_message = str(e)
        logger.error(f"Validation error: {error_message}")
        return ErrorResponse(error="validation_error", message=error_message)
    except Exception as e:
        # General error handling
        error_message = f"Unexpected error: {str(e)}"
        logger.error(error_message, exc_info=True)
        return ErrorResponse(error="server_error", message="An unexpected error occurred while generating the diagram")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting ArchWize API server")
    uvicorn.run(app, host="0.0.0.0", port=8000) 