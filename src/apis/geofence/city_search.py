# locustfile.py
from locust import HttpUser, task, between
from util import constants
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
  def search_cities(self):
    res = self.client.get(
        "/api/v1/cities",
        params={"is_alphabetically_sorted": True, "is_global_city": True},
        headers=self.headers(),
        name="/api/v1/cities"
        )
