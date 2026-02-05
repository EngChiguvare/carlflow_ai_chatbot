def score_lead(text: str):
    text = text.lower()
    score = 0

    if any(k in text for k in ['price', 'quote', 'demo', 'buy', 'meeting', 'call']):
        score += 40
    if any(k in text for k in ['urgent', 'asap', 'now']):
        score += 30
    if len(text.split()) <= 3:
        score += 10

    if score >= 60:
        return score, 'HOT'
    elif score >= 30:
        return score, 'WARM'
    return score, 'COLD'