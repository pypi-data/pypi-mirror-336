from ..utils.string import normalize_string


def _get_partial_similarity(s1_substrings: list[str], s2_substrings: list[str]) -> bool:
    set_a = set(s1_substrings)
    set_b = set(s2_substrings)

    score = 0
    for a in set_a:
        if a in set_b:
            current_score = 1
        else:
            current_score = 0
            for b in set_b:
                if b.startswith(a):
                    current_score = max(current_score, len(a) / len(b))

        score += current_score

    return score / len(set_a)


def get_starts_with_similarity(s1: str, s2: str, normalize: bool = True) -> bool:
    """
    Calculate similarity score based on whether one string starts with another.
    Score is normalized between 0 (no common prefix) and 1 (identical).

    Args:
        s1: First string
        s2: Second string
        normalize: Whether to normalize the strings before comparison

    Returns:
        float: Similarity score between 0 and 1
    """
    if normalize:
        s1 = normalize_string(s1)
        s2 = normalize_string(s2)

    if s1 == s2:
        return 1
    else:
        s1_substrings = s1.split()
        s2_substrings = s2.split()

        score_a = _get_partial_similarity(s1_substrings, s2_substrings)
        score_b = _get_partial_similarity(s2_substrings, s1_substrings)

        weighted_partial_score_a = score_a * len(s1) / (len(s1) + len(s2))
        weighted_partial_score_b = score_b * len(s2) / (len(s2) + len(s1))

        return weighted_partial_score_a + weighted_partial_score_b
