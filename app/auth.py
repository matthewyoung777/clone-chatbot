from fastapi import HTTPException, Security, Request
from fastapi.security.api_key import APIKeyHeader
from starlette import status
from dotenv import load_dotenv
import os

load_dotenv()

# Replace this with the actual API key (you could store it in an environment variable for better security)
CHATBOT_API_KEY = os.environ["CHATBOT_API_KEY"]


api_key = APIKeyHeader(name="X-API-KEY")


async def validate_api_key(req: Request, key: str = Security(api_key)):
    if not key or key != CHATBOT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key",
        )
