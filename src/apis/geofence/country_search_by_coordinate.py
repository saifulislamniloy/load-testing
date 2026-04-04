# locustfile.py
from locust import HttpUser, task, between, TaskSet
from load_testing.util.RandomCoordinateGenerator import RandomCoordinateGenerator
from load_testing.util import constants
BANGLADESH = constants.BANGLADESH
DHAKA = constants.DHAKA
JWT_TOKEN = constants.JWT_TOKEN 

class LocationServiceUser(HttpUser):
  wait_time = between(1, 5)

  def on_start(self):
    # If you have a login endpoint, get token here
    # response = self.client.post("/auth/login", json={"email": "...", "password": "..."})
    # self.token = response.json()["access_token"]
    self.token = JWT_TOKEN

  def headers(self):
    return {"Authorization": f"Bearer {self.token}"}

  @task
  def search_countries(self):
    lat, lon = RandomCoordinateGenerator.random_point_in_polygon(DHAKA)
    self.client.get(
        "/api/v1/countries",
        params={"latitude": lat, "longitude": lon},
        headers=self.headers(),
        name="/api/v1/countries"
        )
