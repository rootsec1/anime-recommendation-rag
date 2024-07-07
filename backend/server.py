from backend.constants import SYSTEM_PROMPT, USER_PROMPT
from util import prompt_llm
from scripts.ingestion import ingest_data
import chromadb
from fastapi import FastAPI, Request, HTTPException
from nltk.corpus import stopwords
# Check and download stopwords
import nltk
nltk.download("stopwords")

# Load stopwords
STOP_WORDS = set(stopwords.words("english"))

app = FastAPI()
chroma_client = chromadb.PersistentClient()
chroma_collection = chroma_client.get_or_create_collection(
    "anime",
    metadata={"hnsw:space": "cosine"}
)
if chroma_collection.count() == 0:
    print("[!] Embedding collection is empty. Ingesting data...")
    ingest_data()


@app.get("/")
async def health_check():
    return {"ping": "pong"}


@app.post("/recommend-anime")
async def recommend_anime(req: Request):
    try:
        data = await req.json()
        prompt = data["prompt"]
        # Remove stopwords from prompt
        cleaned_prompt = " ".join(
            [word for word in str(prompt).split()
             if word.lower() not in STOP_WORDS]
        )
        # Search for similar documents
        similar_docs = chroma_collection.query(
            query_texts=[cleaned_prompt],
            n_results=10
        )
        summary_list = [
            metadata for metadata in similar_docs["metadatas"]
        ][0]
        summary_list = [summary["summary"] for summary in summary_list]
        context = "\n\n".join(summary_list)
        templated_user_prompt = USER_PROMPT.format(
            system_prompt=SYSTEM_PROMPT,
            context=context,
            question=prompt
        )
        print(templated_user_prompt)
        llm_response = prompt_llm(templated_user_prompt)
        return {"recommendation": llm_response}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
