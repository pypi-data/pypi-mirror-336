from ..utils.string import normalize_string


def _get_partial_similarity(
    s1_substrings: list[str],
    s2_substrings: list[str],
    common_prefix_min_ratio: float = 0.66,
) -> bool:
    set_a = set(s1_substrings)
    set_b = set(s2_substrings)

    score = 0
    for a in set_a:
        if a in set_b:
            current_score = 1
        else:
            current_score = 0
            for b in set_b:
                # Find the common prefix length
                common_prefix_len = 0
                min_len = min(len(a), len(b))

                for i in range(min_len):
                    if a[i] != b[i]:
                        break
                    common_prefix_len += 1

                if (common_prefix_len / min_len) >= common_prefix_min_ratio:
                    # Score = 2 * common_prefix_length / (length_a + length_b)
                    current_score = max(
                        current_score, 2 * common_prefix_len / (len(a) + len(b))
                    )

        score += current_score

    return score / len(set_a)


def get_common_prefix_similarity(
    s1: str,
    s2: str,
    common_prefix_min_ratio: float = 0.66,
    normalize: bool = True,
) -> bool:
    """
    Calculate similarity score based on common prefix between strings.
    Score is normalized between 0 (no common prefix) and 1 (identical).

    Args:
        s1: First string
        s2: Second string
        common_prefix_min_ratio: Minimum length of common prefix to consider
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

        score_a = _get_partial_similarity(
            s1_substrings, s2_substrings, common_prefix_min_ratio
        )
        score_b = _get_partial_similarity(
            s2_substrings, s1_substrings, common_prefix_min_ratio
        )

        weighted_partial_score_a = score_a * len(s1) / (len(s1) + len(s2))
        weighted_partial_score_b = score_b * len(s2) / (len(s2) + len(s1))

        return weighted_partial_score_a + weighted_partial_score_b
