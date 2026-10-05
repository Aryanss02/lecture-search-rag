from vector_db import client


COLLECTION_NAME = "lecture_search"


# Delete old collection
if client.collection_exists(COLLECTION_NAME):

    client.delete_collection(
        collection_name=COLLECTION_NAME
    )

    print("Old collection deleted!")


# Create fresh collection
from qdrant_client.models import Distance, VectorParams

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

print("Fresh collection created!")