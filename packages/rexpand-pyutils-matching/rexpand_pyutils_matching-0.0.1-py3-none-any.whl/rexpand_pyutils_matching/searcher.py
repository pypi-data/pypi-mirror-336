"""
This module provides functionality for fuzzy searching and matching text values,
with optional LLM-based exact matching and value suggestion capabilities.
"""

import logging
import random
from rexpand_pyutils_matching.matchers import SimilarityMeasure, SIMILARITY_FUNCTIONS

import json
from rexpand_pyutils_matching.utils.chatgpt import askChatGPT


def fuzzy_search(
    search_key,
    standard_values,
    threshold=None,
    candidate_count=1,
    similarity_measure=SimilarityMeasure.COMMON_PREFIX,
    normalize=True,
):
    """
    Performs fuzzy search to find similar values from a list of standard values.

    Args:
        search_key: The text to search for
        standard_values: List of values to search through
        threshold: Minimum similarity score to consider a match (optional)
        candidate_count: Number of top candidates to return
        similarity_measure: Method to calculate similarity between strings
        normalize: Whether to normalize similarity scores

    Returns:
        List of tuples (value, similarity_score) sorted by similarity
    """
    if threshold is None and candidate_count is None:
        raise ValueError("Either threshold or candidate_count must be provided")

    if candidate_count <= 0:
        raise ValueError("candidate_count must be greater than 0")

    candidates = []
    similarity_func = SIMILARITY_FUNCTIONS[similarity_measure]

    # Calculate similarity scores for each standard value
    for value in standard_values:
        similarity = similarity_func(search_key, value, normalize=normalize)
        if not threshold or similarity >= threshold:
            candidates.append((value, similarity))

    return sorted(candidates, key=lambda x: x[1], reverse=True)[:candidate_count]


def exact_match_check(candidates, exact_match_threshold=1):
    """
    Checks if the top candidate is an exact match based on similarity threshold.

    Args:
        candidates: List of (value, similarity) tuples
        exact_match_threshold: Minimum similarity score to consider an exact match

    Returns:
        The matching value if found, None otherwise
    """
    if candidates[0][1] >= exact_match_threshold:
        return candidates[0][0]
    else:
        return None


def check_exact_match_via_llm(
    search_key, candidate_names, api_key, context_string=None, verbose=False
):
    """
    Uses LLM to check if any candidate is an exact match for the search key.

    Args:
        search_key: The text to match
        candidate_names: List of candidate values to check
        api_key: API key for LLM service
        context_string: Additional context for the matching task
        verbose: Whether to log detailed information

    Returns:
        The exact matching candidate if found, None otherwise
    """
    message = f"Return the candidate that is an exact match for the search key"
    if context_string:
        message += f" given the following context.\nContext: {context_string}"
    else:
        message += "."

    message += f"\nSearch key: {search_key}\nCandidates: {candidate_names}"
    if verbose:
        loggable_message = message.replace("\n", " ")
        logging.info(f"Checking exact match via LLM with message: {loggable_message}")

    response = askChatGPT(
        message=message,
        api_key=api_key,
        text={
            "format": {
                "name": "exact_match",
                "type": "json_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "candidate": {
                            "type": "string",
                            "description": "The candidate that is an exact match for the search key, or 'None' if there is no exact match",
                        },
                    },
                    "required": ["candidate"],
                    "additionalProperties": False,
                },
            }
        },
    )
    return json.loads(response.output_text)["candidate"]


def suggest_new_value_via_llm(
    search_key, candidates, api_key, context_string=None, verbose=False
):
    """
    Uses LLM to suggest a new value based on the search key and existing candidates.

    Args:
        search_key: The text to find a match for
        candidates: List of existing candidate values
        api_key: API key for LLM service
        context_string: Additional context for the suggestion task
        verbose: Whether to log detailed information

    Returns:
        A suggested new value if appropriate, None otherwise
    """
    message = f"Suggest a new candidate for the search key given the following candidate examples"
    if context_string:
        message += f" and context.\nContext: {context_string}"
    else:
        message += "."

    message += f"\nSearch key: {search_key}\nCandidate examples: {candidates}"
    if verbose:
        loggable_message = message.replace("\n", " ")
        logging.info(f"Suggesting new value via LLM with message: {loggable_message}")

    response = askChatGPT(
        message=message,
        api_key=api_key,
        text={
            "format": {
                "name": "suggest_new_value",
                "type": "json_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "candidate": {
                            "type": "string",
                            "description": "The new suggested candidate that is not in the candidate examples, or 'None' if there is no new candidate to suggest",
                        },
                    },
                    "required": ["candidate"],
                    "additionalProperties": False,
                },
            }
        },
    )
    return json.loads(response.output_text)["candidate"]


def search(
    search_key,
    standard_values,
    threshold=None,
    candidate_count=1,
    exact_match_threshold=1,
    similarity_measure=SimilarityMeasure.COMMON_PREFIX,
    normalize=True,
    use_llm_for_exact_match=False,
    use_llm_for_suggestion=False,
    llm_context_string=None,
    chatgpt_api_key=None,
    verbose=False,
):
    """
    Main search function that combines fuzzy search with optional LLM-based matching and suggestion.

    Args:
        search_key: The text to search for
        standard_values: List of values to search through
        threshold: Minimum similarity score for fuzzy search
        candidate_count: Number of top candidates to consider
        exact_match_threshold: Minimum similarity score for exact matching
        similarity_measure: Method to calculate similarity between strings
        normalize: Whether to normalize similarity scores
        use_llm_for_exact_match: Whether to use LLM for exact matching
        use_llm_for_suggestion: Whether to use LLM for suggesting new values
        llm_context_string: Additional context for LLM operations
        chatgpt_api_key: API key for ChatGPT service
        verbose: Whether to log detailed information

    Returns:
        Dictionary containing:
            - candidate: The matched or suggested value
            - is_suggested: Boolean indicating if the result is a suggested value
    """
    # Get candidates via fuzzy search
    candidates = fuzzy_search(
        search_key,
        standard_values,
        threshold=threshold,
        candidate_count=candidate_count,
        similarity_measure=similarity_measure,
        normalize=normalize,
    )
    candidate_names = [candidate[0] for candidate in candidates]
    if verbose:
        logging.info(f"Candidates via fuzzy search: {candidates}")

    # If there are candidates, try to find an exact match
    if len(candidates) > 0:
        # If there is an exact match, return the candidate
        if exact_match_check(candidates, exact_match_threshold):
            if verbose:
                logging.info(f"Exact match found: {candidates[0][0]}")

            return {"candidate": candidates[0][0], "is_suggested": False}

        # There is no exact match, so let the LLM check if there is an exact match if enabled
        if use_llm_for_exact_match:
            candidate_name = check_exact_match_via_llm(
                search_key,
                candidate_names,
                context_string=llm_context_string,
                api_key=chatgpt_api_key,
                verbose=verbose,
            )
            if candidate_name and candidate_name != "None":
                if verbose:
                    logging.info(f"Exact match found via LLM: {candidate_name}")

                return {"candidate": candidate_name, "is_suggested": False}

    if not use_llm_for_suggestion:
        if verbose:
            logging.info(f"No exact match found, and no new value suggested")

        return {"candidate": None, "is_suggested": False}

    # If there are less than 5 candidates, sample some more candidates
    if len(candidates) < 5:
        sample_count = min(5, len(standard_values)) - len(candidates)
        if sample_count > 0:
            candidate_names = candidate_names + random.sample(
                standard_values, sample_count
            )

    # Suggest a new value
    candidate_name = suggest_new_value_via_llm(
        search_key,
        candidates,
        context_string=llm_context_string,
        api_key=chatgpt_api_key,
        verbose=verbose,
    )

    # If the new value is not valid, return None
    if not candidate_name or candidate_name == "None":
        if verbose:
            logging.info(f"No new value suggested")

        return {"candidate": None, "is_suggested": False}

    # Re-validate the new value to ensure it's not too similar to existing values
    revalidated_candidates = fuzzy_search(
        candidate_name,
        standard_values,
        threshold=1,
        candidate_count=1,
        similarity_measure=similarity_measure,
        normalize=normalize,
    )
    is_suggested = not (len(revalidated_candidates) > 0)
    if verbose:
        logging.info(f"Suggested value: {candidate_name}, is_suggested: {is_suggested}")

    return {"candidate": candidate_name, "is_suggested": is_suggested}
