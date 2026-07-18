import requests


class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def register_agent(self, ip_address, tapak_id):

        payload = {
            "ip_address": ip_address,
            "tapak_id": tapak_id
        }

        response = requests.post(
            f"{self.base_url}/ejen/register",
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json()
    
    def get_tasks(self, agent_id):

        response = requests.get(
            f"{self.base_url}/ejen/{agent_id}/tugasan",
            timeout=30
        )

        response.raise_for_status()

        return response.json()
    
    def submit_scan_result(
        self,
        profil_tugasan_id,
        agent_id,
        hasil
    ):

        payload = {
            "profil_tugasan_id": profil_tugasan_id,
            "ejen_id": agent_id,
            "hasil": hasil
        }

        response = requests.post(
            f"{self.base_url}/ejen/hasil",
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        return response.json()
    
    