import random

def TransposeChars(text : str, error_rate : float = 0.1) -> str:
    """
    Simulate OCR errors by swapping int(len(text) * error_rate) characters'
    position of the input string.

    Examples:
        >>> text = "The quick brown fox jumps over the lazy dog."
        >>> transpose_chars(text, 0.05)
        The quick brown fox jumps overt heolazy d g.

    Args:
        - text: A string to elaborate.
        - error_rate: A number between 0 and 1,
            representing the percentage of characters of text that will be swapped.

    Returns:
        string: A string with swapped characters.
    """

    transposed_text = list(text)

    # Determine the number of characters to transpose
    num_errors = int(len(text) * error_rate)

    # Perform transposition errors
    for _ in range(num_errors):
        # Randomly select two indices to swap
        index1 = random.randint(0, len(text) - 1)
        index2 = random.randint(0, len(text) - 1)

        # Swap characters at the selected indices
        transposed_text[index1], transposed_text[index2] = transposed_text[index2], transposed_text[index1]

    return ''.join(transposed_text)


def OcrTransposition(text: str, error_rate: float = 0.1) -> str:
    """
    Simulate OCR errors by swapping int(len(text) * error_rate) words' position of the input string.

    Examples:
        >>> text = "The quick brown fox jumps over the lazy dog."
        >>> ocr_transposition(text, 0.2)
        over quick brown fox jumps The the lazy dog.

    Args:
        - text: A string to elaborate.
        - error_rate: A number between 0 and 1, representing the percentage of words of text that will be swapped.

    Returns:
        string: A string with swapped words.
    """

    words = text.split()
    num_transpositions = int(len(words) * error_rate)

    for _ in range(num_transpositions):
        # Choose two random indexes to change words.
        index1, index2 = random.sample(range(len(words)), 2)
        words[index1], words[index2] = words[index2], words[index1]

    return ' '.join(words)


def SimulateOcrErrors(text : str, error_rate: float = 0.1) -> str:
    """
    Simulate OCR errors by replacing characters with visually similar substitutes.

    Examples:
        >>> text = "I won 1-0 yesterday. I liked to lie a lot. Can I have 222 apples, please?"
        >>> simulate_ocr_errors(text, 0.4)
        I won 1-0 yesterday. l Iiked to lie a Iot. Can I have 2ZZ appIes, please?

    Args:
        - text: A string to elaborate.
        - error_rate: A number between 0 and 1, representing the percentage of words of text that will be swapped.

    Returns:
        string: A string with swapped words.
    """

    similar_chars = {
        'I': 'l',
        'l': 'I',
        '0': 'O',
        'O': '0',
        '1': 'l',
        '2': 'Z',
        'Z': '2'} # Add other similar characters as needed

    error_text = ''
    for char in text:
        if random.random() < error_rate and char in similar_chars:
            # Replace the character with a similar substitute
            error_text += similar_chars[char]
        else:
            error_text += char

    return error_text





