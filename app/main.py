from app.models import AskRequest
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/ask/")
def ask_question(question: AskRequest):
    return {"question": question}
