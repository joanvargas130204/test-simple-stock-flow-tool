import requests
from typing import Optional, Dict, Any, List

class ApiClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip("/")
        self.token: Optional[str] = None

    def login(self, username: str, password: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/auth/login"
        resp = requests.post(url, json={"username": username, "password": password})
        resp.raise_for_status()
        data = resp.json()
        self.token = data.get("accessToken")
        return data

    def register_seller(self, username: str, password: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/auth/register"
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.post(url, json={"username": username, "password": password, "role": "seller"}, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def get_categories(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/api/categories"
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def create_product(self, name: str, price: float, stock: int, category_id: str) -> str:
        url = f"{self.base_url}/api/products"
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.post(url, json={
            "name": name,
            "price": price,
            "stock": stock,
            "categoryId": category_id
        }, headers=headers)
        resp.raise_for_status()
        return resp.json()["id"]

    def place_sale(self, lines: List[Dict[str, Any]]) -> str:
        url = f"{self.base_url}/api/sales"
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.post(url, json={"lines": lines}, headers=headers)
        resp.raise_for_status()
        return resp.json()["id"]

    def get_health(self) -> Dict[str, Any]:
        url = f"{self.base_url}/health"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
