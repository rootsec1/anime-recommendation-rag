from backend.constants import SYSTEM_PROMPT, USER_PROMPT
from backend.util import prompt_llm
from scripts.ingestion import ingest_data
import chromadb
from fastapi import FastAPI, Request, HTTPException
from nltk.corpus import stopwords
# Check and download stopwords
import nltk
nltk.download("stopwords")

# Load stopwords from the English language to filter out in processing.
STOP_WORDS = set(stopwords.words("english"))

# Initialize the FastAPI app
app = FastAPI()

# Initialize a persistent client to interact with ChromaDB
chroma_client = chromadb.PersistentClient()
# Get or create a collection named 'anime' with specific metadata for the HNSW algorithm
chroma_collection = chroma_client.get_or_create_collection(
    "anime",
    metadata={"hnsw:space": "cosine"}
)

# Check if the collection is empty and ingest data if it is.
if chroma_collection.count() == 0:
    print("[!] Embedding collection is empty. Ingesting data...")
    ingest_data()


@app.get("/")
async def health_check():
    """
    Health check endpoint to ensure the service is running.

    Returns:
        dict: A simple JSON response indicating the service is alive.
    """
    return {"ping": "pong"}


@app.post("/recommend-anime")
async def recommend_anime(req: Request):
    """
    Endpoint to recommend anime based on a user's prompt.

    Args:
        req (Request): The request object containing the user's prompt.

    Returns:
        dict: A dictionary containing the recommendation.

    Raises:
        HTTPException: If any error occurs during processing.
    """
    try:
        # Extract the JSON data from the request
        data = await req.json()
        prompt = data["prompt"]

        # Remove stopwords from the prompt to clean it for better search results
        cleaned_prompt = " ".join(
            [word for word in str(prompt).split()
             if word.lower() not in STOP_WORDS]
        )

        # Search for similar documents in the ChromaDB collection
        similar_docs = chroma_collection.query(
            query_texts=[cleaned_prompt],
            n_results=10
        )

        # Extract summaries from the search results
        summary_list = [
            metadata for metadata in similar_docs["metadatas"]
        ][0]
        summary_list = [summary["summary"] for summary in summary_list]

        # Concatenate summaries to form a context for the LLM
        context = "\n\n".join(summary_list)

        # Format the user prompt with the system prompt and context
        templated_user_prompt = USER_PROMPT.format(
            system_prompt=SYSTEM_PROMPT,
            context=context,
            question=prompt
        )

        # Print the templated prompt for debugging
        print(templated_user_prompt)

        # Generate a recommendation using the LLM
        llm_response = prompt_llm(templated_user_prompt)

        return {"recommendation": llm_response}
    except Exception as ex:
        # Raise an HTTP 500 error if any exception occurs
        raise HTTPException(status_code=500, detail=str(ex))
