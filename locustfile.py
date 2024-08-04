from locust import HttpUser, task


class AnimeRecommenderUser(HttpUser):
    wait_time = None  # No wait time between tasks

    @task
    def health_check(self):
        # Test the health check endpoint
        self.client.get("/")

    @task
    def recommend_anime(self):
        # Test the recommend_anime endpoint
        payload = {
            "prompt": "I'm looking for an anime similar to Naruto."
        }
        self.client.post("/recommend-anime", json=payload)
