#!/usr/bin/env python3

import os

from common.binary_inventory import list_kernel_modules

from common.binary_profile import BinaryProfile

from common.binary_metadata import guess_language

from common.crypto_detection import detect_crypto

from common.confidence import calculate_overall_confidence

from common.json_exporter import export_json

from common.platform_utils import get_crypto_deps 


def main():

    profiles = []

    modules = list_kernel_modules()

    total = len(modules)

    for index, module in enumerate(modules, start=1):

        print(
            f"[{index}/{total}] Processing: {module}"
        )

        profile = BinaryProfile(

            path=module,

            filename=os.path.basename(module),

            extension=os.path.splitext(module)[1].lstrip("."),
        )

        profile.language = guess_language(module)

        libs = get_crypto_deps(module)

        if libs != "none":
            profile.crypto_dependencies = libs.split(",")

        hits = detect_crypto(module)

        profile.detections = hits

        profile.overall_confidence = (
            calculate_overall_confidence(profile)
        )

        profiles.append(profile)



    json_result = export_json(profiles)

    return json_result


def run_scan():
    return main()


if __name__ == "__main__":
    main()