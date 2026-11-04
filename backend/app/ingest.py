from qdrant_client.models import PointStruct

from app.parser import read_lecture
from app.chunker import create_chunks
from app.embeddings import create_embedding
from app.vector_db import client


# ============================================================
# CONFIG
# ============================================================

COLLECTION_NAME = "lecture_search_fastembed"

BATCH_SIZE = 25


# ============================================================
# 1. READ LECTURE
# ============================================================

lecture = read_lecture(
    "data/lectures/lecture_01.txt"
)

chunks = create_chunks(
    lecture["segments"]
)

print("Total chunks:", len(chunks))


# ============================================================
# 2. CREATE POINTS
# ============================================================

points = []

for index, chunk in enumerate(chunks):

    embedding = create_embedding(
        chunk["text"]
    )

    point = PointStruct(
        id=index,

        vector=embedding.tolist(),

        payload={
            "text": chunk["text"],
            "video_title": chunk["video_title"],
            "video_url": chunk["video_url"],
            "start_time": chunk["start_time"],
            "end_time": chunk["end_time"],
            "timestamp_url": chunk["timestamp_url"]
        }
    )

    points.append(point)


print("Embeddings created:", len(points))


# ============================================================
# 3. UPLOAD TO QDRANT IN BATCHES
# ============================================================

total_points = len(points)

for start in range(
    0,
    total_points,
    BATCH_SIZE
):

    end = min(
        start + BATCH_SIZE,
        total_points
    )

    batch = points[start:end]

    print(
        f"\nUploading batch "
        f"{start + 1}-{end} "
        f"of {total_points}..."
    )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=batch
    )

    print(
        f"Uploaded {end}/{total_points}"
    )


# ============================================================
# 4. COMPLETE
# ============================================================

print("\n======================================")
print("INGESTION COMPLETE")
print("======================================")
print("Uploaded chunks:", total_points)