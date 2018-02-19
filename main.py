from nltk.tokenize import sent_tokenize, word_tokenize
import pyphen

def main():
    with open("input.txt", "r") as f:
        input_data = f.read()

    cword = calculate_words(input_data)

    print ("Word count: " + str(cword))
    [wordmap, csyllable] = calculate_syllables(input_data)

    # print ("Words->syllable count: ", wordmap)

    print ("Syllable count: " + str(csyllable))

    csentence = calculate_sentences(input_data)

    print("Sentence count: " + str(csentence))

    score = calculate_formula(cword, csentence, csyllable)

    print ("Score: " + str(score))

def calculate_formula(words, sentences, syllables):
    """Calculates the Flesch-Kincaid Reading Ease Formula"""
    return 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables/words))


def calculate_words(text):
    """Return the number of words in the inputted text."""
    count = 0
    worker = pyphen.Pyphen(lang='nl_NL')

    for word in word_tokenize(text):
       if word.isalpha():
            count += 1

    return count

def calculate_sentences(text):
    """Return the number of sentences in the inputted text."""
    return len(sent_tokenize(text))

def calculate_syllables(text):
    """Return the number of syllables in the inputted text.""" 
    # Set up return struct and syllable function
    count = 0
    wordmap = {}
    worker = pyphen.Pyphen(lang='nl_NL')
    
    # count syllables 
    for word in word_tokenize(text):
       if word.isalpha():
        word = worker.inserted(word)
        wordmap[word] = word.count('-')
        if word.count('-') == 0:
            count += 1
        else:
            count += word.count('-')

    return wordmap, count

main()