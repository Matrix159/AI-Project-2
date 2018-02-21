from nltk.tokenize import sent_tokenize, word_tokenize
import pyphen


def main():
    calculate_category("Online news", "./online-news/", "online-news-info.txt")
    calculate_category("Trump tweets", "./tweets/", "trumpt-tweets.txt")

def calculate_category(category_name, input_folder, output_file):
    """
    Prints reading ease information for each text source in a category
    to a text file.
    :param category_name: The name of the category
    :param input_folder: The folder name to read files from
    :param output_file: The output file for the category
    :return: None
    """
    open(output_file, 'w').close()
    for x in range(1, 11):
        with open(input_folder + "input{}.txt".format(str(x)), "r", encoding="utf8") as f:
            input_data = f.read()
        with open(output_file, 'a') as out:
            out.write(category_name + " {}".format(str(x)) + '\n')
            cword = calculate_words(input_data)
            out.write("Word count: " + str(cword) + "\n")
            [wordmap, csyllable] = calculate_syllables(input_data)
            out.write("Syllable count: " + str(csyllable) + "\n")
            csentence = calculate_sentences(input_data)
            out.write("Sentence count: " + str(csentence) + "\n")
            score = calculate_formula(cword, csentence, csyllable)
            out.write("Score: " + str(score) + "\n\n\n")


def calculate_formula(words, sentences, syllables):
    """
    Calculates the Flesch-Kincaid Reading Ease Formula.
    :param words: Number of words
    :param sentences: Number of sentences
    :param syllables: Number of syllables
    :return: Reading ease formula result
    """
    return 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables/words))


def calculate_words(text):
    """
    Return the number of words in the inputted text.
    :param text: Input text
    :return: Number of words
    """
    count = 0
    #worker = pyphen.Pyphen(lang='nl_NL')
    for word in word_tokenize(text):
        if word.isalpha():
            count += 1

    return count


def calculate_sentences(text):
    """
    Return the number of sentences in the inputted text.
    :param text: Input text
    :return: Number of sentences
    """
    return len(sent_tokenize(text))


def calculate_syllables(text):
    """
    Return the number of syllables in the inputted text.
    :param text: Input text
    :return: Number of syllables
    """
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
