from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from services import DiagramService

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

class DiagramRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "ArchWize Backend Running!"}

@app.post("/generate")
async def generate_diagram(request: DiagramRequest):
    try:
        # Use the DiagramService to generate the diagram
        mermaid_code = await DiagramService.generate_mermaid_diagram(request.prompt)
        return {"mermaid_code": mermaid_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 