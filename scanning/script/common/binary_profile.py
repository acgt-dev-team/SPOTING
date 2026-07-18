from dataclasses import dataclass, field


@dataclass
class BinaryProfile:
    """
    Represents everything known about one binary.
    This is the single source of truth used by all exporters.
    """

    # -----------------------------
    # Basic information
    # -----------------------------
    path: str
    filename: str
    extension: str

    # -----------------------------
    # Metadata
    # -----------------------------
    language: str = "Unknown"
    architecture: str = "Unknown"
    state: str = "Unknown"
    signed: bool = False

    # -----------------------------
    # Libraries
    # -----------------------------
    system_libraries: list = field(default_factory=list)
    third_party_libraries: list = field(default_factory=list)
    crypto_dependencies: list = field(default_factory=list)

    # -----------------------------
    # Crypto findings
    # -----------------------------
    detections: list = field(default_factory=list)

    # -----------------------------
    # Overall summary
    # -----------------------------
    overall_confidence: str = "Unknown"