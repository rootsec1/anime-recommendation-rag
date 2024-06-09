import uuid
import chromadb
import pandas as pd
from tqdm import tqdm
from nltk.corpus import stopwords
# Check and download stopwords
import nltk
nltk.download("stopwords")

# Load stopwords
STOP_WORDS = set(stopwords.words("english"))


def create_summary(title: str, synopsis: str, mal_link: str) -> str:
    return f"Title: {title}\nSynopsis: {synopsis}\nMyAnimeList link: {mal_link}".strip()


def ingest_data():
    FILE_PATH = "data/raw/anime.csv"
    chroma_client = chromadb.PersistentClient()
    chroma_collection = chroma_client.get_or_create_collection(
        "anime",
        metadata={"hnsw:space": "cosine"}
    )
    if chroma_collection.count() > 0:
        print("[!] Collection already has data. Please clear the collection before ingesting new data.")
        return

    print("[*] Ingesting data...")
    # Read CSV
    df = pd.read_csv(FILE_PATH, encoding="utf-8")
    df = df.dropna()
    df = df.drop_duplicates()

    print("[*] Creating summaries...")
    # Create Summary list
    df["summary"] = df.apply(
        lambda x: create_summary(x["title"], x["synopsis"], x["link"]),
        axis=1
    )
    summary_list = df["summary"].tolist()

    print("[*] Creating embeddings and ingesting documents...")
    for summary in tqdm(summary_list):
        # Remove stop words from the summary
        summary_cleaned = " ".join([word for word in str(summary).split()
                                    if word.lower() not in STOP_WORDS])
        summary_hash = str(uuid.uuid4())
        chroma_collection.add(
            documents=[summary_cleaned],
            metadatas=[{"summary": summary}],
            ids=[summary_hash]
        )

    print("="*50)
    print("[+] Data ingestion complete.")
    print(f"[+] Collection has {chroma_collection.count()} documents.")
    print("[+] Top 10 documents:")
    print(chroma_collection.peek())


if __name__ == "__main__":
    ingest_data()
