from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
import pyphen


def main():

    calculate_category("Online news", "./online-news/", "online-news-info.txt")
    calculate_category("Trump tweets", "./tweets/", "trump-tweets.txt")
    increase_difficulty("Online news difficulty increase", "./online-news/", "online-news-info-diff-increase.txt")
    increase_difficulty("Trump tweets difficulty increase", "./tweets/", "trump-tweets-diff-increase.txt")


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
    average_sum = 0
    for x in range(1, 11):
        with open(input_folder + "input{}.txt".format(str(x)), "r", encoding="utf8") as f:
            input_data = f.read()
        with open(output_file, 'a') as out:
            out.write(category_name + " {}".format(str(x)) + '\n')
            cword = calculate_words(input_data)
            out.write("Word count: " + str(cword) + "\n")
            wordmap, csyllable = calculate_syllables(input_data)
            out.write("Syllable count: " + str(csyllable) + "\n")
            csentence = calculate_sentences(input_data)
            out.write("Sentence count: " + str(csentence) + "\n")
            score = calculate_formula(cword, csentence, csyllable)
            average_sum += score
            out.write("Score: " + str(score) + "\n\n\n")
            if x == 10:
                out.write("Score average: " + str(average_sum/10))


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
    worker = pyphen.Pyphen(lang='en')
    
    # count syllables 
    for word in word_tokenize(text):
        if word.isalpha():
           word = worker.inserted(word)
           wordmap[word] = word.count('-')
           if word.count('-') == 0:
               count += 1
           else:
               count += word.count('-')+1

    return wordmap, count


def increase_difficulty(category_name, input_folder, output_file):
    """
    Increases the reading difficulty of the text by increasing syllables count
    using synonyms.
    :param category_name: The name of the category
    :param input_folder: The folder name to read files from
    :param output_file: The output file for the category
    :return: None
    """
    open(output_file, 'w').close()
    average_sum = 0
    for x in range(1, 11):
        with open(input_folder + "input{}.txt".format(str(x)), "r", encoding="utf8") as f:
            input_data = f.read()
        with open(output_file, 'a') as out:
            old_syllable_count = 0
            new_syllable_count = 0
            # Go through and find synonyms for each word and take the one
            # with the most syllables as our new syllable count for that word.
            for word in word_tokenize(input_data):
                if word.isalpha():
                    worker = pyphen.Pyphen(lang='en')
                    old_word = word
                    old_word_hyph = worker.inserted(old_word)
                    old_word_count = 0
                    new_word_count = 0

                    if old_word_hyph.count('-') == 0:
                        old_word_count += 1
                    else:
                        old_word_count += old_word.count('-')+1
                    old_syllable_count += old_word_count
                    previous_new_count = old_word_count
                    # if word in dictionary:
                    for syn in wn.synsets(old_word):
                        for l in syn.lemmas():
                            new_word = l.name()
                            # count syllables
                            new_word_hyph = worker.inserted(new_word)
                            if new_word_hyph.count('-') == 0:
                                new_word_count += 1
                            else:
                                new_word_count += new_word_hyph.count('-')+1
                            if new_word_count > previous_new_count:
                                previous_new_count = new_word_count
                    new_syllable_count += previous_new_count
            out.write(category_name + " {}".format(str(x)) + '\n')
            cword = calculate_words(input_data)
            out.write("Word count: " + str(cword) + "\n")
            out.write("Syllable count: " + str(new_syllable_count) + "\n")
            csentence = calculate_sentences(input_data)
            out.write("Sentence count: " + str(csentence) + "\n")
            score = calculate_formula(cword, csentence, new_syllable_count)
            average_sum += score
            out.write("Score: " + str(score) + "\n\n\n")
            if x == 10:
                out.write("Score average: " + str(average_sum / 10))

main()
