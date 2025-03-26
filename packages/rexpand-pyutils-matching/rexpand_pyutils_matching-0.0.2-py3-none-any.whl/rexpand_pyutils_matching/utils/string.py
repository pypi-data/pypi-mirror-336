# Define common special_s to be replaced with spaces
special_chars = [
    "/",
    ",",
    ";",
    "-",
    "_",
    "|",
    "\\",
    "+",
    "&",
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    "?",
    "!",
    ".",
    " ",
]


# Normalize both strings by replacing special_s with spaces and converting to lowercase
def normalize_string(text: str) -> str:
    text = text.lower()
    for special_char in special_chars:
        text = text.replace(special_char, " ")
    return text
