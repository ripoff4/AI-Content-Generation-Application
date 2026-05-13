from fastapi import FastAPI
from pydantic import BaseModel
from backend.graph.graph import agent

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserRequest(BaseModel):
    user_question: str


@app.get("/")
def home():
    return {
        "message": "AI Content Research Agent API Running"
    }


@app.post("/generate")
def generate_content(request: UserRequest):

    result = agent.invoke({
        "user_question": request.user_question
    })

    return {
        "response": result["response"]
    }
