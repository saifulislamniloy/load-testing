# locustfile.py
from locust import HttpUser, task, between, TaskSet
from load_testing.util.RandomCoordinateGenerator import RandomCoordinateGenerator

# --- CONFIG ---
JWT_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiI5MGEyZmZjMS1mMTY1LTQ2NDktOGIyZS1jMDJiYmQxNTA3MTIiLCJzdWIiOiI4MDA2OTc4NzY0Mzg5MTMwMjQiLCJpYXQiOjE3NzI1OTc3MDQsImV4cCI6MTc3MzIwMjUwNCwidG9rZW5fdmVyIjoxLCJkZXZpY2VfaWQiOiJzdHJpbmciLCJzdWJfdHlwZSI6IkRSSVZFUiIsInNpZCI6ImI5N2VkYTBjLTI4NjUtNDg2OS1hZjljLTYzMzk0YWQ2MDc5ZiIsInJvbGVzIjpbIlJPTEVfRFJJVkVSIl19.Zie25X8XoM58adEzGfpapae8W5IFxcAi5D5tJKTsjgyeEwmfOfrtj91PDCqMSJhjXrkKc1RCTWs7QNEYncGnDg"  # paste your token here
# Or use on_start to login dynamically if you have a login endpoint

class LocationServiceUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # If you have a login endpoint, get token here
        # response = self.client.post("/auth/login", json={"email": "...", "password": "..."})
        # self.token = response.json()["access_token"]
        self.token = JWT_TOKEN

    def headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    # ── High frequency: read/query endpoints ──────────────────────

    @task
    def find_zone_by_location(self):
        """Most likely your hottest endpoint"""

        lat, lon = RandomCoordinateGenerator.random_point_in_polygon()
        print(lat, lon)
        res = self.client.get(
            f"/api/v1/zones/location",
            params={"latitude": {lat}, "longitude": {lon}},
            headers=self.headers(),
            name="/api/v1/zones/location"
        )

        print(res.status_code, res.text)
