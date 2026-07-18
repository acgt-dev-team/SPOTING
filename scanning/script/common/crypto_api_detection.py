import copy

from .crypto_api_rules import CRYPTO_API_RULES
from .os_utils import OS_TYPE

if OS_TYPE == "windows":
    from .windows_utils import get_imported_functions
else:
    from .linux_utils import get_imported_functions


def detect_crypto_apis(binary):
    apis = get_imported_functions(binary)

    hits = []

    for api in apis:
        if api not in CRYPTO_API_RULES:
            continue

        info = copy.deepcopy(CRYPTO_API_RULES[api])

        info["api"] = api
        info["confidence"] = "high"
        info["detection_source"] = {
            f'{info["library"]} Import API'
        }

        hits.append(info)

    return hits