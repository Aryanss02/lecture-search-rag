from groq import Groq
from dotenv import load_dotenv
import os

from app.embeddings import create_embedding
from app.vector_db import client


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GROQ CLIENT
# ============================================================

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ============================================================
# QDRANT COLLECTION
# ============================================================

COLLECTION_NAME = "lecture_search"


# ============================================================
# RETRIEVE RELEVANT LECTURE CHUNKS
# ============================================================

def retrieve_context(query, limit=3):

    # Convert user question into an embedding
    query_vector = create_embedding(query).tolist()

    # Search Qdrant
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True
    ).points

    return results


# ============================================================
# BUILD CONTEXT FOR THE LLM
# ============================================================

def build_context(results):

    context_parts = []

    for result in results:

        payload = result.payload

        context_parts.append(
            f"""
Lecture: {payload['video_title']}
Timestamp: {payload['start_time']} seconds

Content:
{payload['text']}
"""
        )

    return "\n\n".join(context_parts)




# ============================================================
# GENERATE ANSWER USING GROQ
# ============================================================

def generate_answer(query, context):

    prompt = f"""
You are an AI learning assistant.

Answer the user's question using ONLY the lecture context
provided below.

If the answer is not present in the lecture context,
say that the lecture does not provide enough information
to answer the question.

Do not invent information.

Explain the answer clearly and simply.

LECTURE CONTEXT:
{context}

USER QUESTION:
{query}
"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI learning assistant that answers questions using provided lecture context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# ============================================================
# BUILD SOURCE INFORMATION
# ============================================================

def build_sources(results):

    sources = []

    for result in results:

        payload = result.payload

        sources.append({
            "video_title": payload["video_title"],
            "start_time": payload["start_time"],
            "end_time": payload["end_time"],
            "timestamp_url": payload["timestamp_url"]
        })

    return sources




if __name__ == "__main__":

    query = "What is cricket?"

    results = retrieve_context(query)

    context = build_context(results)

    answer = generate_answer(
        query,
        context
    )

    sources = build_sources(results)

    print("\n======================================")
    print("AI ANSWER")
    print("======================================")

    print(answer)

    print("\n======================================")
    print("SOURCES")
    print("======================================")

    for source in sources:

        print("\nVideo:", source["video_title"])
        print("Start:", source["start_time"], "seconds")
        print("End:", source["end_time"], "seconds")
        print("Watch:", source["timestamp_url"])