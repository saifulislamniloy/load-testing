# locustfile.py
from locust import HttpUser, task, between, TaskSet
JWT_TOKEN = constants.JWT_TOKEN 


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

    @task(10)
    def find_zone_by_location(self):
        """Most likely your hottest endpoint"""
        self.client.get(
            "/api/v1/zones/location",
            params={"latitude": 23.780007, "longitude": 90.416147},
            headers=self.headers(),
            name="/api/v1/zones/location"
        )

    @task(10)
    def get_restriction_by_location(self):
        self.client.get(
            "/api/v1/get-restriction/location",
            params={
                "latitude": 23.780007,
                "longitude": 90.416147,
                "serviceType": "car",
                "serviceOption": "economy",
                "tripType": "inner_city"
            },
            headers=self.headers(),
            name="/api/v1/get-restriction/location"
        )

    @task(8)
    def get_rules_by_location(self):
        self.client.get(
            "/api/v1/get-rules/location",
            params={
                "latitude": 23.794901542739417,
                "longitude": 90.41422162328628,
                "rule_type": "surge"
            },
            headers=self.headers(),
            name="/api/v1/get-rules/location"
        )

    @task(8)
    def find_nearby_participants(self):
        self.client.get(
            "/api/v1/locations/search",
            params={
                "source": "DRIVER",
                "latitude": 23.794181,
                "longitude": 90.415588,
                "radius": 2,
                "service_type": "car",
                "service_option": "economy"
            },
            headers=self.headers(),
            name="/api/v1/locations/search"
        )

    @task(5)
    def search_zones(self):
        self.client.get(
            "/api/v1/zones",
            params={"city_id": 1, "is_active": True},
            headers=self.headers(),
            name="/api/v1/zones"
        )

    @task(5)
    def search_rules(self):
        self.client.get(
            "/api/v1/rules/search",
            params={"rule_type": "surge", "page": 0, "size": 10},
            headers=self.headers(),
            name="/api/v1/rules/search"
        )

    # ── Medium frequency ──────────────────────────────────────────

    @task(3)
    def search_cities(self):
        self.client.get(
            "/api/v1/cities",
            params={"status": True},
            headers=self.headers(),
            name="/api/v1/cities"
        )

    @task(3)
    def get_service_types(self):
        self.client.get(
            "/api/v1/service-type",
            params={"city_code": "DKK"},
            headers=self.headers(),
            name="/api/v1/service-type"
        )

    @task(3)
    def find_trip_type(self):
        self.client.post(
            "/api/v1/cities/trip-type",
            json={
                "source_location": {"latitude": 23.85055, "longitude": 90.40021},
                "pickup": {"latitude": 23.85061, "longitude": 90.40870},
                "drop": {"latitude": 23.79456, "longitude": 90.41388},
                "destination": {"latitude": 23.79440, "longitude": 90.41384},
                "stoppages": []
            },
            headers=self.headers(),
            name="/api/v1/cities/trip-type"
        )

    @task(2)
    def get_pickup_drop_city_info(self):
        self.client.post(
            "/api/v1/cities/pickup-drop-info",
            json={
                "source_location": {"latitude": 23.85055, "longitude": 90.40021},
                "pickup": {"latitude": 23.85061, "longitude": 90.40870},
                "drop": {"latitude": 23.79456, "longitude": 90.41388},
                "destination": {"latitude": 23.79440, "longitude": 90.41384},
                "stoppages": []
            },
            headers=self.headers(),
            name="/api/v1/cities/pickup-drop-info"
        )

    @task(2)
    def check_participant_existence(self):
        self.client.post(
            "/api/v1/locations/participant-existence-check",
            json={
                "source": "driver",
                "pickup_latitude": 23.800127,
                "pickup_longitude": 90.415886,
                "participant_id": "765817976990838784",
                "radius_list_in_meter": [300, 500]
            },
            headers=self.headers(),
            name="/api/v1/locations/participant-existence-check"
        )

    # ── Low frequency: admin/config reads ────────────────────────

    @task(1)
    def search_countries(self):
        self.client.get(
            "/api/v1/countries",
            headers=self.headers(),
            name="/api/v1/countries"
        )

    @task(1)
    def health_check(self):
        self.client.get("/", headers=self.headers(), name="/")