# **clone-chatbot**

**Purpose:**  
The `clone-chatbot` serves as the backend for a chatbot that uses Retrieval-Augmented Generation (RAG) to act as a clone of me, providing conversational responses about my background, work, and other related topics.

---

## **Features:**

- **RAG-powered**: Retrieves context from a PostgreSQL database containing relevant content (e.g., background, projects, skills).
- **LLM Integration**: Uses OpenAI API for generating responses based on retrieved context.
- **Python FastAPI**: Fast and efficient backend API for querying the chatbot.

---

## How it works:

### Data Preparation

##### 1. Prepare Data

Information about me is first prepared, descriptions for work experience, project details, education etc. Metadata is also added to provide extra context to the information for LLMs and RAG to use to speed up relevance search and retrieval.

##### 2. Chunking the Data

The data is then broken down into smaller parts, a process called "chunking". This is important because only so much text can be used as input for embedding models, so chunks must be small enough to be processed.
Markdown header level chunking structure:

- Projects (1)
  - ProjectName (2)
    - Overview(2)
    - Features(2)
    - TechStack(2)
- Work Experience (1)
  - Role Name + Desc (2)
- Interests (1)
  - Interest Name (2)

##### 3. Generate Embeddings for Vector Database

A text embedding model like OpenAI's `text-embedding-ada-002` is used to create embeddings (vectors) for each chunk to then be stored in the vector database.
For example a row would look like:

```json
{
    "id": 1,
    "category": "hobbies"
    "text": "I really loves soccer and basketball...",
    "embedding": [0.42848024, 0.38188, ...],
}
```

### Retrieval (Querying the Database)

##### 1. Embedding the query

A user asks a question(query), which is then used with the same embedding model as before to generate an embedding
`"Does Matt like any sports?" -> embedding model -> [0.238204, 0.042880, ...]`

##### 2. Vector simliarity Search

Most relevant documents are found by taking the vector embedding of the query, and finding the nearest vectors by calculating cosine similarity in the vector database.

### Augmentation

##### 1. Combining retrieved chunks

The most relevant chunks of data are then compiled to form context to be used to answer the question

##### 2. Prompt Engineering

A custom prompt is constructed containing the retrieved chunks and the user's question.

### Generation

##### 1. Prompt is sent to LLM (GPT-4)

LLM will decide if the given context is relevant to the question, and generates an answer based off of that decision which is then returned as a response.

---

## **Setup Instructions:**

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/clone-chatbot.git
cd clone-chatbot
```

### 2. Set up environment

```bash
# create virtual environment
python -m venv venv
# activate the virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate      # Windows
# install dependencies
pip install -r requirements.txt
```

### 3. Run the app

```bash
uvicorn main:app --reload
```

OR

```bash
fastapi dev main.py
```

for auto reload
OR

```bash
fastapi run main.py
```

for production
