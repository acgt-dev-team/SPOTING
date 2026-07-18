from common.api_client import APIClient

client = APIClient("http://localhost:8000")

agent = client.register_agent(
    ip_address="127.0.0.1",
    tapak_id=10
)

print("Agent:")
print(agent)

tasks = client.get_tasks(agent["id"])

print("\nTasks:")
print(tasks)