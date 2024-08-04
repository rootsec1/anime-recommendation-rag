from locust import HttpUser, task, between


class HealthCheckUser(HttpUser):
    wait_time = between(1, 3)  # Run health check more frequently

    @task
    def health_check(self):
        # Test the health check endpoint
        self.client.get("/")


class AnimeRecommenderUser(HttpUser):
    wait_time = between(180, 240)  # 3-4 minutes between tasks

    @task
    def recommend_anime(self):
        # Test the recommend_anime endpoint
        payload = {
            "prompt": "If I like anime like Naruto and One Piece, what should I watch next?"
        }
        self.client.post("/recommend-anime", json=payload)
