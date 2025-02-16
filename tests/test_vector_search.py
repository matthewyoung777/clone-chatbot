from app.utils import insert_embedding, search_similar_vectors

# Example vector (adjust based on your embedding model)
example_vector = [0.1] * 1536

# Insert data
insert_embedding("This is a test sentence.", example_vector)

# Query similar vectors
results = search_similar_vectors(example_vector)
print(results)
