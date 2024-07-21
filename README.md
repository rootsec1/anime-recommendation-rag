## Anime Recommender RAG based LLM

![Pipeline Status](https://github.com/rootsec1/anime-recommendation-rag/actions/workflows/build-docker-image.yml/badge.svg)
![Pipeline Status](https://github.com/rootsec1/anime-recommendation-rag/actions/workflows/format-and-test.yml/badge.svg)

## Dockerfile

[Dockerhub link](https://hub.docker.com/r/abhishekwl/anime-recommendation-backend)

## Final Demo Video

[click here](https://www.loom.com/share/7b3b3b3b1b7e4b3e8)

## Project Purpose

There are several sources for getting anime recommendations such as MyAnimeList, Reddit and so on. However, the scores could be biased and sometimes anime fans like myself go down a rabbit hole digging through subreddits and so on to find the perfect anime to watch. This project aims to solve this problem by providing a chatbot interface where users can ask for anime recommendations based on their preferences. The chatbot uses the LLM model to generate responses and provide recommendations.

## Architecture Diagram

<img width="733" alt="Screenshot 2024-07-20 at 8 17 00 PM" src="https://github.com/user-attachments/assets/70e9fe29-2b7b-49e9-a5df-8c51e6699a28">

## Instructions

#### Setup

1. Download [llava-v1.5-7b-q4.llamafile](https://huggingface.co/Mozilla/llava-v1.5-7b-llamafile/resolve/main/llava-v1.5-7b-q4.llamafile?download=true) (4.29 GB).

2. Open your computer's terminal.

3. If you're using macOS, Linux, or BSD, you'll need to grant permission
   for your computer to execute this new file. (You only need to do this
   once.)

```sh
chmod +x llava-v1.5-7b-q4.llamafile
```

4. If you're on Windows, rename the file by adding ".exe" on the end.

5. Run the llamafile. e.g.:

```sh
./llava-v1.5-7b-q4.llamafile
```

6. Your browser should open automatically and display a chat interface.
   (If it doesn't, just open your browser and point it at http://localhost:8080)

7. When you're done chatting, return to your terminal and hit
   `Control-C` to shut down llamafile.

8. Clone the repository

```sh
git clone git@github.com:rootsec1/anime-recommendation-rag.git
```

9. Change directory to the cloned repository

```sh
cd anime-recommendation-rag
```

10. Install the dependencies

```sh
pip install -r requirements.txt
```

#### Running the application

1. Start the FastAPI server

```sh
PYTHONPATH=. fastapi dev backend/server.py
```

2. Start the streamlit frontend application

```sh
streamlit run frontend/ui.py
```

#### Testing the application

1. Run the tests

```sh
PYTHONPATH=. pytest backend/test_server.py --disable-pytest-warnings -v
```

2. Screenshot of unit tests
   <img width="866" alt="Screenshot 2024-07-20 at 8 18 50 PM" src="https://github.com/user-attachments/assets/8d99682c-382d-4e93-aae9-c02a3d647124">

## Application Screenshots

<img width="771" alt="Screenshot 2024-06-29 at 4 08 38 PM" src="https://github.com/rootsec1/anime-recommendation-rag/assets/20264867/961efd88-f877-46e9-9de6-1937392396e2">
