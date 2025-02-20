from app.embeddings import search_embeddings, generate_query_embedding

# Example vector (adjust based on your embedding model)


query = "What is the tech stack of Forge Fitness?"
query_embedding = generate_query_embedding(query)

# %%
search_results = search_embeddings(query_embedding)

# %%
for result in search_results:
    print(f"Content: {result[0]}")
