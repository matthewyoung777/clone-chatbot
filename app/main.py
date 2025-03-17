from app.models import AskRequest, AskResponse
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from app.queries import process_query
from app.auth import validate_api_key
import lorem

app = FastAPI(dependencies=[Depends(validate_api_key)])
origins = [
    "http://localhost:3000",  # Local development
    "https://matthewyoung.info",  # Production frontend URL
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)

# Initialize rate limiter (tracks requests by IP)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


# Custom handler for rate limit errors
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests. Please wait and try again later."},
    )


@app.get("/")
# @limiter.limit("5/minute")
def read_root(request: Request):
    return {"answer": lorem.paragraph()}


@app.get("/wake")
def wake_up(request: Request):
    return {"answer": "I'm awake"}


@app.post("/ask", response_model=AskResponse)
@limiter.limit("10/minute")
def ask_question(
    request: Request,
    question: AskRequest,
):
    answer = process_query(question.question)
    return AskResponse(answer=answer)
