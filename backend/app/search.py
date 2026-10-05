from sentence_transformers import SentenceTransformer

from vector_db import client


COLLECTION_NAME = "lecture_search"

model = SentenceTransformer("all-MiniLM-L6-v2")


query = "What arithmetic operations can we perform with numbers in Python?"

query_vector = model.encode(query).tolist()


results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=10,
    with_payload=True
).points


print("======================================")
print("SEARCH RESULTS")
print("======================================")


for index, result in enumerate(results, start=1):

    print(f"\nResult {index}")
    print("------------------------------")

    print("Score:", result.score)
    print("Text:", result.payload["text"])
    print("Video:", result.payload["video_title"])
    print("Start time:", result.payload["start_time"])
    print("Watch:", result.payload["timestamp_url"])