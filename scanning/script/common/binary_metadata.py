from common.platform_utils import run_strings


# ===================================================================
# GUESS PROGRAMMING LANGUAGE
# ===================================================================

def guess_language(binary_path):
    """
    Guess the programming language used to build a binary by
    inspecting embedded strings.
    """

    signatures = {
        "Go": [
            "go.runtime",
            "runtime.gopanic",
        ],
        "Rust": [
            "rustc/",
            "rust_panic",
        ],
        "Python": [
            "Py_Initialize",
            "python",
        ],
        "C++": [
            "GLIBCXX",
            "std::",
        ],
        "Java": [
            "JNI_CreateJavaVM",
            "java/lang/Object",
        ],
    }

    try:
        output = run_strings(binary_path).lower()

        for lang, sigs in signatures.items():
            if any(sig.lower() in output for sig in sigs):
                return lang

        return "C"

    except Exception:
        return "Unknown"