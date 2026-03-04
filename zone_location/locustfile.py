# locustfile.py
from locust import HttpUser, task, between, TaskSet

# --- CONFIG ---
JWT_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiI3MmVjYzBkZC03NzM5LTQxMDQtYmMzOS0xOGU1YmJiOWY3YmIiLCJzdWIiOiI4MDA2OTc4NzY0Mzg5MTMwMjQiLCJpYXQiOjE3NzIzMzkxODQsImV4cCI6MTc3Mjk0Mzk4NCwidG9rZW5fdmVyIjoxLCJkZXZpY2VfaWQiOiJzdHJpbmciLCJzdWJfdHlwZSI6IkRSSVZFUiIsInNpZCI6IjhhYzY0ZDQ0LTI3NGItNGI4NS04NzgwLTk3NTBmMjg5M2EwNyIsInJvbGVzIjpbIlJPTEVfRFJJVkVSIl19.JwN3wMOdbA_2ASHBmGFDURr5i4q-nKjHhTxkMJwELmrS_Pd-u9RuE_lXuJyULgMIjhHcGsgYR2cXDIFS_sfmHw"  # paste your token here
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
        self.client.get(
            "/api/v1/zones/location",
            params={"latitude": 23.780007, "longitude": 90.416147},
            headers=self.headers(),
            name="/api/v1/zones/location"
        )
