import os
from groq import Groq
from utils.ingestor import get_collection

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

def answer_question(question: str, top_k: int = 5) -> dict:
    collection = get_collection()

    results = collection.query(
        query_texts=[question],
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    docs = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not docs:
        return {
            "answer": "No relevant documents found. Please upload and ingest documents first.",
            "sources": []
        }

    context = "\n\n".join([
        f"[Source: {meta['source']}, Chunk {meta['chunk']}]\n{doc}"
        for doc, meta in zip(docs, metadatas)
    ])

    sources = list(set([meta["source"] for meta in metadatas]))

    client = Groq(api_key=GROQ_API_KEY)

    system_prompt = """You are a healthcare investment due diligence assistant for Valtruis, 
a value-based care investment firm. You answer questions based strictly on the provided 
document context. Be concise, factual, and highlight any risks or opportunities relevant 
to healthcare investment decisions. If the answer is not in the context, say so clearly."""

    user_prompt = f"""Context from uploaded documents:
{context}

Question: {question}

Answer based only on the context above. Be specific and cite which document the information comes from."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
        max_tokens=1000
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }