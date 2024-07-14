import uuid
import chromadb
import pandas as pd
from tqdm import tqdm
from nltk.corpus import stopwords
# Check and download stopwords to ensure they are available for processing
import nltk
nltk.download("stopwords")

# Load stopwords from the English language to filter out in processing.
STOP_WORDS = set(stopwords.words("english"))


def create_summary(title: str, synopsis: str, mal_link: str) -> str:
    """
    Creates a formatted summary string combining title, synopsis, and MyAnimeList link.

    Args:
        title (str): The title of the anime.
        synopsis (str): The synopsis of the anime.
        mal_link (str): The MyAnimeList link for the anime.

    Returns:
        str: A formatted summary string.
    """
    return f"Title: {title}\nSynopsis: {synopsis}\nMyAnimeList link: {mal_link}".strip()


def ingest_data():
    """
    Ingests anime data from a CSV file into a ChromaDB collection.

    Reads anime data from a specified CSV file, cleans and processes the data,
    and then ingests it into a ChromaDB collection with generated embeddings.
    """
    FILE_PATH = "data/raw/anime.csv"  # Path to the CSV file containing anime data
    # Initialize a persistent client to interact with ChromaDB
    chroma_client = chromadb.PersistentClient()
    chroma_collection = chroma_client.get_or_create_collection(
        "anime",
        # Specify metadata for the collection, using cosine space for HNSW algorithm
        metadata={"hnsw:space": "cosine"}
    )
    # Check if the collection already contains data
    if chroma_collection.count() > 0:
        print("[!] Collection already has data. Please clear the collection before ingesting new data.")
        return

    print("[*] Ingesting data...")
    # Read the CSV file, drop any rows with missing values, and remove duplicates
    df = pd.read_csv(FILE_PATH, encoding="utf-8").dropna().drop_duplicates()

    print("[*] Creating summaries...")
    # Generate a summary for each row in the dataframe
    df["summary"] = df.apply(
        lambda x: create_summary(x["title"], x["synopsis"], x["link"]),
        axis=1
    )
    # Convert the summary column to a list
    summary_list = df["summary"].tolist()

    print("[*] Creating embeddings and ingesting documents...")
    # Use tqdm to display a progress bar
    for summary in tqdm(summary_list, desc="Ingesting documents"):
        # Clean the summary by removing stopwords
        summary_cleaned = " ".join([word for word in str(
            summary).split() if word.lower() not in STOP_WORDS])
        # Generate a unique identifier for the document
        summary_hash = str(uuid.uuid4())
        # Add the cleaned summary to the ChromaDB collection
        chroma_collection.add(
            documents=[summary_cleaned],
            metadatas=[{"summary": summary}],
            ids=[summary_hash]
        )

    print("="*50)
    print("[+] Data ingestion complete.")
    print(f"[+] Collection has {chroma_collection.count()} documents.")
    print("[+] Top 10 documents:")
    # Display the top 10 documents in the collection
    print(chroma_collection.peek())


if __name__ == "__main__":
    ingest_data()  # Run the ingest_data function if the script is executed directly
