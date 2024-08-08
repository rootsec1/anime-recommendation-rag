## Anime Recommender RAG based LLM

![Pipeline Status](https://github.com/rootsec1/anime-recommendation-rag/actions/workflows/build-docker-image.yml/badge.svg)
![Pipeline Status](https://github.com/rootsec1/anime-recommendation-rag/actions/workflows/format-and-test.yml/badge.svg)

## Dockerfile

[Dockerhub link](https://hub.docker.com/r/abhishekwl/anime-recommendation-backend)

## Final Demo Video

[click here](https://duke.box.com/s/6ie1vld6z2693xd3b1uttvl5ojf4l09r)

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
(or run using the Docker image)
docker run --platform linux/x86_64 -e MODEL_URL=http://127.0.0.1:8080/v1/chat/completions -p 8000:8000 --network="host" abhishekwl/anime-recommendation-backend
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

### Performance Report (Load Testing using Locust)

| Type | Name             | Request Count | Failure Count | Median Response Time | Average Response Time | Min Response Time | Max Response Time | Average Content Size | Requests/s | Failures/s | 50%    | 66%    | 75%    | 80%    | 90%    | 95%    | 98%    | 99%    | 99.9%  | 99.99% | 100%   |
| ---- | ---------------- | ------------- | ------------- | -------------------- | --------------------- | ----------------- | ----------------- | -------------------- | ---------- | ---------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| GET  | /                | 386           | 0             | 5000.0               | 5100.0                | 4900.0            | 5200.0            | 0.0                  | 7.5583     | 0.0        | 5000   | 5050   | 5100   | 5120   | 5150   | 5180   | 5190   | 5195   | 5200   | 5200   | 5200   |
| POST | /recommend-anime | 54            | 0             | 155000.0             | 151417.85             | 71608.70          | 227882.48         | 1821.0               | 0.237      | 0.0        | 155000 | 155000 | 228000 | 228000 | 228000 | 228000 | 228000 | 228000 | 228000 | 228000 | 228000 |
|      | Aggregated       | 440           | 0             | 155000.0             | 26668.36              | 4900.0            | 227882.48         | 1821.0               | 7.7953     | 0.0        | 5000   | 5050   | 228000 | 228000 | 228000 | 228000 | 228000 | 228000 | 228000 | 228000 | 228000 |

This performance report summarizes the results of load testing conducted on our API endpoints using Locust. The tests were performed on a MacBook Air with the following specifications:

```plaintext
Hardware Overview:

   Model Name: MacBook Air
   Model Identifier: Mac14,2
   Chip: Apple M2
   Total Number of Cores: 8 (4 performance and 4 efficiency)
   Memory: 16 GB
   System Firmware Version: 10151.121.1
   OS Loader Version: 10151.121.1
```

This setup was used to assess the API's responsiveness and reliability under concurrent requests.

- **GET `/` Endpoint**: The health check endpoint was tested with 386 requests. The average response time was approximately 5.1 seconds, with no failures, showcasing consistent performance under load.

- **POST `/recommend-anime` Endpoint**: The recommendation endpoint was tested with 54 requests. The response times exhibited significant variance, with a median of 155 seconds. Despite the higher latency, the endpoint successfully handled all requests without any failures.

The test results indicate that the system can handle multiple requests concurrently without errors, though optimizations may be required to reduce response times for the recommendation endpoint under heavier loads.
