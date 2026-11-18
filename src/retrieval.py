from .config import TOP_K

def semantic_retrieve(vectorstore, query, k=TOP_K):
    # relevance scores are convenient for thresholding/debugging
    return vectorstore.similarity_search_with_relevance_scores(query, k=k)

def retrieve_documents(vectorstore, query, k=TOP_K, threshold=0.20):
    scored = semantic_retrieve(vectorstore, query, k)
    accepted = [(doc, score) for doc, score in scored if score >= threshold]
    return accepted if accepted else scored[:min(2, len(scored))]
