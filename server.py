"""
FastAPI server for OpenEnv Medical OCR Environment
Exposes step(), reset(), state() endpoints for HF Spaces
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
from environment import MedicalOCREnv, Action, Observation, Reward
import uvicorn


app = FastAPI(title="Medical OCR OpenEnv", version="1.0.0")

# Enable CORS for HF Spaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance
env: Optional[MedicalOCREnv] = None


class ResetRequest(BaseModel):
    task_id: str = "easy_printed_prescription"


class StepRequest(BaseModel):
    action: Dict[str, Any]


class StepResponse(BaseModel):
    observation: Dict[str, Any]
    reward: Dict[str, Any]
    done: bool
    info: Dict[str, Any]


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "name": "Medical Prescription OCR Environment",
        "version": "1.0.0",
        "status": "running",
        "openenv": True
    }


@app.post("/reset")
async def reset(request: Optional[ResetRequest] = None) -> Dict[str, Any]:
    """Reset environment to initial state"""
    global env
    
    try:
        # Use default task if no request body provided
        task_id = request.task_id if request else "easy_printed_prescription"
        env = MedicalOCREnv(task_id=task_id)
        observation = env.reset()
        return {"observation": observation.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/step")
async def step(request: StepRequest) -> StepResponse:
    """Execute action and return new state"""
    global env
    
    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    try:
        # Parse action
        action = Action(**request.action)
        
        # Execute step
        observation, reward, done, info = env.step(action)
        
        return StepResponse(
            observation=observation.model_dump(),
            reward=reward.model_dump(),
            done=done,
            info=info
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/state")
async def state() -> Dict[str, Any]:
    """Return current environment state"""
    global env
    
    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    return env.state()


@app.get("/tasks")
async def list_tasks() -> Dict[str, Any]:
    """List available tasks"""
    return {
        "tasks": [
            {
                "id": "easy_printed_prescription",
                "difficulty": "easy",
                "description": "Extract text from clear, printed prescription"
            },
            {
                "id": "medium_handwritten_prescription",
                "difficulty": "medium",
                "description": "Extract text from handwritten prescription"
            },
            {
                "id": "hard_complex_prescription",
                "difficulty": "hard",
                "description": "Extract and structure data from complex multi-drug prescription"
            }
        ]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
