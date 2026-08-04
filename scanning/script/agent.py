import json
import platform
import socket
import time
import traceback

from common.api_client import APIClient
from common.scanner_dispatcher import execute_task
from machine_id import get_machine_id


# ---------------------------------------
# Load configuration
# ---------------------------------------
with open("config.json", "r") as f:
    config = json.load(f)

BASE_URL = config["backend_url"]
TAPAK_ID = config["tapak_id"]
PROFILE_ID = config["profile_id"]


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

    hostname = platform.node()
    machine_id = get_machine_id()

    # ---------------------------------------
    # Register Agent
    # ---------------------------------------
    while True:
        try:

            print("========================================")
            print("Registering Agent")
            print("========================================")
            print(f"Hostname   : {hostname}")
            print(f"Machine ID : {machine_id}")
            print(f"IP Address : {get_local_ip()}")
            print(f"Tapak ID   : {TAPAK_ID}")
            print(f"Profile ID : {PROFILE_ID}")
            print()

            agent = client.register_agent(
                ip_address=get_local_ip(),
                tapak_id=TAPAK_ID,
                profile_id=PROFILE_ID,
                machine_id=machine_id,
                hostname=hostname
            )

            agent_id = agent["id"]

            print(f"Agent registered successfully.")
            print(f"Agent ID : {agent_id}")
            print()

            break

        except Exception:
            print("\nFailed to register agent.")
            traceback.print_exc()
            print("Retrying in 10 seconds...\n")
            time.sleep(10)

    # ---------------------------------------
    # Main polling loop
    # ---------------------------------------
    while True:

        try:

            print("----------------------------------------")
            print("Polling for pending tasks...")
            print("----------------------------------------")

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
