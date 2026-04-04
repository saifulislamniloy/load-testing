# locustfile.py
from locust import HttpUser, task, between, TaskSet
from load_testing.util.RandomCoordinateGenerator import RandomCoordinateGenerator
from load_testing.util import constants
BANGLADESH = constants.BANGLADESH
DHAKA = constants.DHAKA
JWT_TOKEN = constants.JWT_TOKEN 

class LocationServiceUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.token = JWT_TOKEN

    def headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    
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

        # print(payload)

        res = self.client.post(
            "/api/v1/cities/trip-type",
            json=payload,
            headers=self.headers(),
            name="/api/v1/cities/trip-type"
        )

        print(res.status_code, res.text)