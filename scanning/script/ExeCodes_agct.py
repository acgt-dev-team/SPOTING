import os

from common.binary_inventory import list_script_files
from common.script_utils import scan_file

from common.binary_profile import BinaryProfile
from common.json_exporter import export_json
from common.confidence import calculate_overall_confidence



def main():

    profiles = []

    scripts = list_script_files()

    total = len(scripts)

    for index, script in enumerate(scripts, start=1):

        print(f"[{index}/{total}] Processing: {script}")

        hits = scan_file(script)

        if not hits:
            continue

        profile = BinaryProfile(
            path=script,
            filename=os.path.basename(script),
            extension=os.path.splitext(script)[1].lstrip("."),
        )

        profile.detections = hits
        profile.overall_confidence = calculate_overall_confidence(profile)

        profiles.append(profile)

    json_result = export_json(profiles)

    return json_result

def run_scan():
    print(">>> run_scan called <<<", flush=True)
    return main()


if __name__ == "__main__":
    main()

    