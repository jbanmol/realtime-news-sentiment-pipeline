from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from pipeline import run_pipeline

app = FastAPI(title="DataFlow Systems Pipeline PoC")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for this PoC
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class ProcessRequest(BaseModel):
    email: str
    source: str

class ProcessResponse(BaseModel):
    items: List[dict]
    notificationSent: bool
    processedAt: str
    errors: List[str]

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/process")
def process_data_info():
    return {"message": "Use POST method to trigger the pipeline, or visit / for the interactive UI."}

@app.post("/process", response_model=ProcessResponse)
async def process_data(request: ProcessRequest):
    """
    Trigger the data enrichment pipeline.
    """
    try:
        # Run pipeline synchronously for simplicity in this PoC to return the results in the response
        # In a real rigorous production system this might be a background task with a callback or polling
        results = await run_pipeline(request.email, request.source)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
