
from fastembed import TextEmbedding

# Load lightweight ONNX embedding model
model = TextEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_embedding(text: str):
    return next(model.embed([text]))
