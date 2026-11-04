from qdrant_client.models import VectorParams, Distance
from app.vector_db import client

COLLECTION_NAME = "lecture_search_fastembed"

if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )
    print("Collection created successfully!")
else:
    print("Collection already exists!")