from common.api_client import APIClient

client = APIClient("http://localhost:8000")

dummy_result = {
    "scan": {
        "scanner": "TEST"
    },
    "binaries": []
}

response = client.submit_scan_result(
    profil_tugasan_id=1,
    agent_id=8,
    hasil=dummy_result
)

print(response)