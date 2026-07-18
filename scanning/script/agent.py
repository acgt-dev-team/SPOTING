import time

from common.api_client import APIClient
from common.scanner_dispatcher import execute_task


BASE_URL = "http://127.0.0.1:8000"


def main():

    client = APIClient(BASE_URL)

    # Register / update agent
    agent = client.register_agent(
        ip_address="127.0.0.1",
        tapak_id=10
    )

    agent_id = agent["id"]

    print(f"Registered Agent ID: {agent_id}")

    while True:

        tasks = client.get_tasks(agent_id)

        if not tasks:
            print("No pending tasks.")
            time.sleep(10)
            continue

        for task in tasks:

            print(f"\nRunning: {task['kod']}")

            try:

                result = execute_task(task)

                client.submit_scan_result(
                    profil_tugasan_id=task["profil_tugasan_id"],
                    agent_id=agent_id,
                    hasil=result
                )

                print("Upload complete.")

            except Exception as e:

                print(e)

        time.sleep(10)


if __name__ == "__main__":
    main()