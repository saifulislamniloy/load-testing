# locustfile.py
from locust import HttpUser, task, between, TaskSet
from load_testing.util.RandomCoordinateGenerator import RandomCoordinateGenerator
from load_testing.util import constants
BANGLADESH = constants.BANGLADESH
DHAKA = constants.DHAKA

# --- CONFIG ---
JWT_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJqdGkiOiI2ZmJjMjM5NS0yM2FkLTQyOTktYWM5ZC1jNmY3MGMxNWRmZjMiLCJzdWIiOiI4MDA2OTc4NzY0Mzg5MTMwMjQiLCJpYXQiOjE3NzI2MDUwMDcsImV4cCI6MTc3MzIwOTgwNywidG9rZW5fdmVyIjoxLCJkZXZpY2VfaWQiOiJzdHJpbmciLCJzdWJfdHlwZSI6IkRSSVZFUiIsInNpZCI6IjMyODljOGRjLTYwYTQtNDM3Yy1hMWZjLTc1MTk3NGFjZjRmMyIsInJvbGVzIjpbIlJPTEVfRFJJVkVSIl19.5MFdRXaAghNQWTloDI661_-wH5MLzGXn_VFbxLSvMvbBxXfVpbQ08Qb3GK7EZsBVzPQEfwtdNxdpkOqD7OFTRQ"  # paste your token here
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

        lat, lon = RandomCoordinateGenerator.random_point_in_polygon(DHAKA)
        print(lat, lon)
        res = self.client.get(
            f"/api/v1/zones/location",
            params={"latitude": {lat}, "longitude": {lon}},
            headers=self.headers(),
            name="/api/v1/zones/location"
        )

        print(res.status_code, res.text)

    
    @task
    def find_trip_type(self):
        """Hit trip-type endpoint with dynamically generated coordinates"""
        # Generate source, pickup, drop, destination
        source_lat, source_lon = RandomCoordinateGenerator.random_point_in_polygon(DHAKA)
        pickup_lat, pickup_lon = RandomCoordinateGenerator.random_point_in_polygon(DHAKA)
        drop_lat, drop_lon = RandomCoordinateGenerator.random_point_in_polygon(DHAKA)
        dest_lat, dest_lon = RandomCoordinateGenerator.random_point_in_polygon(DHAKA)
        stoppage_lat, stoppage_lon = RandomCoordinateGenerator.random_point_in_polygon(DHAKA)

        payload = {
            "source_location": {"latitude": source_lat, "longitude": source_lon},
            "pickup": {"latitude": pickup_lat, "longitude": pickup_lon},
            "drop": {"latitude": drop_lat, "longitude": drop_lon},
            "destination": {"latitude": dest_lat, "longitude": dest_lon},
            "stoppages": [{"latitude": stoppage_lat, "longitude": stoppage_lon}]
        }

        print(payload)

        res = self.client.post(
            "/api/v1/cities/trip-type",
            json=payload,
            headers=self.headers(),
            name="/api/v1/cities/trip-type"
        )

        print(res.status_code, res.text)