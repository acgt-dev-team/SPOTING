def calculate_overall_confidence(profile):
    """
    Calculate an overall confidence score for a BinaryProfile.
    """

    if not profile.crypto_dependencies:
        return "none"

    if not profile.detections:
        return "low"

    ranking = {
        "low": 1,
        "medium": 2,
        "high": 3,
        "very_high": 4,
    }

    highest = "low"

    for hit in profile.detections:
        confidence = hit.get("confidence", "low")

        if ranking[confidence] > ranking[highest]:
            highest = confidence

    return highest