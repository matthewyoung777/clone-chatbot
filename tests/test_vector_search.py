import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.queries import ask_gpt
from app.db import search_embeddings
from app.embeddings import generate_query_embedding


def main():
    while True:
        query = input("Enter your question (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break

        # Generate query embedding
        query_embedding = generate_query_embedding(query)

        # Run a vector similarity search and return the results (chunks)
        search_results = search_embeddings(query_embedding)

        # Get the answer from ask_gpt
        answer = ask_gpt(search_results, query)

        # Print the answer
        print(answer.content)


if __name__ == "__main__":
    main()
