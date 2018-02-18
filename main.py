with open("input.txt", "r") as f:
    input_data = f.read()

print(input_data)


def calculate_formula(words, sentences, syllables):
    """Calculates the Flesch-Kincaid Reading Ease Formula"""
    return 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables/words))


def calculate_words(text):
    """Return the number of words in the inputted text."""
    return 0

def calculate_sentences(text):
    """Return the number of sentences in the inputted text."""
    return 0

def calculate_syllables(text):
    """Return the number of syllables in the inputted text."""
    return 0