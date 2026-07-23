import time
import socket
import traceback

from common.api_client import APIClient
from common.scanner_dispatcher import execute_task
from machine_id import get_machine_id

import json

with open("config.json", "r") as f:
    config = json.load(f)

BASE_URL = config["backend_url"]
TAPAK_ID = config["tapak_id"]


def get_local_ip():
    """
    Returns the local IP address of this machine.
    Falls back to 127.0.0.1 if detection fails.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():

    client = APIClient(BASE_URL)

    # -----------------------------
    # Register agent
    # -----------------------------
    while True:
        try:
            print("Registering agent...")

            agent = client.register_agent(
                ip_address=get_local_ip(),
                tapak_id=TAPAK_ID          # Change this if deploying to another tapak
            )

            agent_id = agent["id"]

            print(f"Registered Agent ID: {agent_id}")

            machine_id = get_machine_id()

            print(f"Machine ID: {machine_id}")
            break

        except Exception:
            print("\nFailed to register agent.")
            traceback.print_exc()
            print("Retrying in 10 seconds...\n")
            time.sleep(10)

    # -----------------------------
    # Main polling loop
    # -----------------------------
    while True:

        try:

            print("\n----------------------------------------")
            print("Polling for pending tasks...")

            tasks = client.get_tasks(agent_id)

            print(f"Tasks received: {len(tasks)}")

            if not tasks:
                print("No pending tasks.")
                time.sleep(10)
                continue

            for task in tasks:

                try:

                    print("----------------------------------------")
                    print(f"Running task: {task['kod']}")
                    print("----------------------------------------")

                    print("Executing scanner...")
                    result = execute_task(task)

                    print("Scanner completed.")
                    print("Uploading results...")

                    client.submit_scan_result(
                        profil_tugasan_id=task["profil_tugasan_id"],
                        agent_id=agent_id,
                        machine_id=machine_id,
                        hasil=result
                    )

                    print("Upload complete.")

                except Exception:
                    print("\nTask failed:")
                    traceback.print_exc()

            print("Waiting for next polling cycle...")
            time.sleep(10)

        except Exception:
            print("\nPolling loop failed:")
            traceback.print_exc()
            print("Retrying in 10 seconds...")
            time.sleep(10)


if __name__ == "__main__":
    main()