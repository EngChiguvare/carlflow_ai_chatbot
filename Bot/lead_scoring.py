def score_lead(text):
    # ✅ Guard against None or empty messages
    if not text or not isinstance(text, str):
        return 0, "COLD"

    text = text.lower()
    score = 0

    hot = ["price", "quote", "demo", "meeting", "call", "book"]
    urgent = ["urgent", "asap", "now", "immediately"]

    if any(word in text for word in hot):
        score += 40

    if any(word in text for word in urgent):
        score += 30

    if len(text.strip()) < 6:
        score += 10

    if score >= 60:
        return score, "HOT"
    elif score >= 30:
        return score, "WARM"
    else:
        return score, "COLD"
