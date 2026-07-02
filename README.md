# Due Diligence RAG Assistant

A natural language due diligence assistant for healthcare investment teams. Upload pitch decks, 10-Ks, and company reports and ask questions across all of them instantly — no more manual document hunting.

## What it does

- Upload multiple PDFs (pitch decks, annual reports, CMS documents, whitepapers)
- System chunks, embeds, and indexes them into a local vector database (ChromaDB)
- Ask any question in plain English
- Get cited, accurate answers pulled directly from your documents

## Built for

Healthcare investment teams doing due diligence across large document sets — built with Valtruis's value-based care investment thesis in mind.

## Stack

- **Frontend:** Streamlit
- **Vector DB:** ChromaDB (local, persistent)
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **LLM:** Groq (llama3-8b) — free tier available
- **PDF parsing:** pypdf

## Setup

```bash
# Clone the repo
git clone https://github.com/RomirHiremath/valtruis-rag-demo
cd valtruis-rag-demo

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key (free at console.groq.com)
export GROQ_API_KEY=your_key_here

# Run the app
streamlit run app.py
```

## How it works

1. PDFs are parsed and split into 500-word overlapping chunks
2. Each chunk is embedded using a local sentence-transformer model
3. Chunks and embeddings are stored in a persistent ChromaDB vector database
4. On query, the question is embedded and the top 5 most similar chunks are retrieved
5. Retrieved chunks are passed as context to an LLM (Groq/llama3) which answers the question and cites sources

## Example questions

- "What is this company's revenue model?"
- "What are the key risks mentioned?"
- "How does this company define value-based care?"
- "Who are the main competitors?"
- "What are the growth projections for next year?"

## Author

Romir Hiremath — [linkedin.com/in/romirhiremath](https://linkedin.com/in/romirhiremath)
