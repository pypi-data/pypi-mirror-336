import requests
from rapidfuzz import fuzz
from rapidfuzz.utils import default_process


def translate_text(
    text: str,
    sl: str = None,
    dl: str = "en",
) -> dict:
    """
    Translate text from one language to another.

    Args:
        text (str): The text to be translated.
        sl (str, optional): The source language code (e.g., 'en' for English, 'es' for Spanish). If not provided, the API will attempt to detect the source language.
        dl (str, optional): The destination language code (default is 'en' for English).


     Returns:
        dict: A dictionary containing the following keys:
            - 'source-text': The original text.
            - 'source-language': The detected or provided source language code.
            - 'destination-text': The translated text.
            - 'destination-language': The destination language code.
    """
    if sl:
        url = f"https://ftapi.pythonanywhere.com/translate?sl={sl}&dl={dl}&text={text}"
    else:
        url = f"https://ftapi.pythonanywhere.com/translate?dl={dl}&text={text}"

    response = requests.get(url)
    response_json = response.json()
    result = {
        "source-text": response_json["source-text"],
        "source-language": response_json["source-language"],
        "destination-text": response_json["destination-text"],
        "destination-language": response_json["destination-language"],
    }
    return result


def are_strings_similar(str1: str, str2: str, threshold: int = 80) -> bool:
    """
    Determine if two strings are similar based on a given threshold.

    Args:
        str1 (str): First string to compare.
        str2 (str): Second string to compare.
        threshold (int, optional): Similarity threshold. Defaults to 80.

    Returns:
        bool: True if the strings are similar, otherwise False.
    """
    str1 = translate_text(str1)["destination-text"]
    str2 = translate_text(str2)["destination-text"]

    similarity_score = fuzz.WRatio(str1, str2, processor=default_process)
    return similarity_score > threshold


def separate_artists(artists: str, custom_separator: str = None) -> list[str]:
    """
    Separate artist names of a song or album into a list.

    Args:
        artists (str): Artists string (e.g., artistA & artistB, artistA ft. artistB).
        custom_separator (str, optional): A specific separator to use. Defaults to None.

    Returns:
        list[str]: List of individual artists.
    """
    default_separators = [";", "/", "ft.", "ft", "feat", "feat.", "with", "&", "and"]

    if custom_separator:
        separators = [custom_separator]
    else:
        separators = default_separators

    for sep in separators:
        artists = artists.replace(sep, ",")

    return [artist.strip() for artist in artists.split(",") if artist.strip()]


def is_valid_string(string: str) -> bool:
    """Validate if a string is non-empty, alphanumeric, or contains non-whitespace characters."""
    return bool(string and (string.isalnum() or not string.isspace()))


if __name__ == "__main__":
    separate_artists("Artist A ft. Artist B")
