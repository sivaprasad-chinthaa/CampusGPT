from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from .config import EMBEDDING_MODEL, INDEX_DIR

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device":"cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

def build_vectorstore(chunks):
    if not chunks: raise ValueError("No document chunks available.")
    return FAISS.from_documents(chunks, get_embeddings())

def save_vectorstore(store, path=INDEX_DIR):
    Path(path).mkdir(parents=True, exist_ok=True)
    store.save_local(str(path))

def load_vectorstore(path=INDEX_DIR):
    return FAISS.load_local(str(path), get_embeddings(), allow_dangerous_deserialization=True)
