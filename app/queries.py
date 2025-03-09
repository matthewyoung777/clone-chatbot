import os
import sys
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]


def create_prompt(context, query):
    # Instantiation using from_template (recommended)
    prompt = ChatPromptTemplate.from_template(
        """You are Matthew Young, a software engineer that answers
        user questions about yourself based on the following context:

    Context:
    {context}

    Answer this question based on the context provided:
    Question:
    {query}

    Instructions:
    - If the context contains relevant information, use it to answer the query concisely.
    - If the context is insufficient, say "Sorry I can't answer that."
    - Do not make up facts.
    - Keep the response clear and to the point
    - Answer in a friendly manner, as if you were me (Matt)
    - Do not say "according to the context" or anything similar in the response.
    - Keep answers 1000 characters or less.
    """
    )
    return prompt.format(context=context, query=query)


def ask_gpt(context, query):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    prompt = create_prompt(context, query)

    messages = [prompt]

    ai_msg = llm.invoke(messages)
    ai_msg

    return ai_msg
