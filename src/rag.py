from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from .config import GROQ_MODEL

SYSTEM = """You are CampusGPT, a helpful university knowledge assistant.
Use ONLY the supplied context to answer. If the answer is not supported by the context, say: "I couldn't find enough information in the available university documents to answer that."
Do not invent policies, dates, fees, eligibility rules, or facts. Keep answers clear and student-friendly. Do not fabricate citations; citations are shown separately from retrieved metadata.
"""

def contextualize_question(question, history):
    # Basic, free implementation: include a short textual history in the final prompt.
    # Advanced query rewriting is intentionally left for later projects.
    return question

def answer_question(question, retrieved, history, api_key):
    if not retrieved:
        return "I couldn't find enough information in the available university documents to answer that."
    context_parts=[]
    sources=[]
    for doc, score in retrieved:
        source=doc.metadata.get('source','Unknown')
        page=doc.metadata.get('page','?')
        context_parts.append(f"SOURCE: {source}, PAGE: {page}\n{doc.page_content}")
        sources.append({"source":source,"page":page,"score":float(score),"text":doc.page_content})
    history_text="\n".join([f"{m['role']}: {m['content']}" for m in history[-6:]])
    prompt=ChatPromptTemplate.from_messages([
        ("system", SYSTEM),
        ("human", "Conversation history:\n{history}\n\nContext:\n{context}\n\nQuestion: {question}")
    ])
    llm=ChatGroq(model=GROQ_MODEL, groq_api_key=api_key, temperature=0.1)
    chain=prompt | llm
    response=chain.invoke({"history":history_text,"context":"\n\n---\n\n".join(context_parts),"question":question})
    return response.content, sources
