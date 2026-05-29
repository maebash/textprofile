import re
import argparse

import nltk

from nltk.corpus import cmudict


cmu = cmudict.dict()


def file_to_str(filepath):
    # takes a filepath and returns a string with the contents of that file
    with open(filepath, 'r') as file:
        file_content = file.read()
    file_content = file_content.replace('\u2019', "'").replace('\u2018', "'")
    return(file_content)


def str_to_words(txtstring):
    # takes a string and returns a list of all words in the string
    word_list = re.findall(r"[a-z]+(?:'[a-z]+)*", txtstring.lower())
    '''
    The regex here looks for all characters between a and z, and accepts them
    until it reaches a non a-z character, except for an apostrophy, at which case
    it continues until the end of the word, keeping the contractions intact.
    '''
    return word_list


def word_frequency_dict(word_list):
    # takes a list of words and returns a dictionary of each unique word and the number of times it occurs
    frequency_dict = {}
    for word in (word_list):
        if word not in frequency_dict:
            frequency_dict[word] = 1
        else:
            frequency_dict[word] += 1
    return frequency_dict


def ttr(word_list):
    # takes a list of words and returns the type-token-ratio
    return len(word_frequency_dict(word_list))/len(word_list)


def hapax_legomena(word_list):
    # takes a list of words and returns a list of the words that only occur once
    word_freq = word_frequency_dict(word_list)
    hapax_legomena_list = [word for word, freq in word_freq.items() if freq == 1]
    return hapax_legomena_list


def hapax_token_ratio(word_list):
    # takes a list of words and returns the hapax/token ratio
    return len(hapax_legomena(word_list))/len(word_list)

    
def hapax_type_ratio(word_list):
    # takes a list of words and returns the hapax/type ratio
    return len(hapax_legomena(word_list))/len(word_frequency_dict(word_list))


def avg_word_length(word_list):
    # takes a list of words and returns the average length of all the words in the list
    temp = [len(word) for word in word_list]
    avg = sum(temp) / len(word_list)
    return avg


def syllable_count(word):
    # takes a word and returns the count of syllables
    count = 0
    # find syllable count using the 0, 1, 2 stress markers in CMU
    if word in cmu:
        for phone in cmu[word][0]:
            if phone[-1].isdigit():
                count += 1
    
    # if not in the CMU dictionary, count clusters of vowels
    # this process will overcount syllables in words with final -e
    else:
        vowel_clusters = re.findall(r"[aeiou]+", word.lower()) 
        count = len(vowel_clusters)
        
    # if a word still has 0 syllables, make it 1
    if count == 0:
        count = 1
        
    return count


def avg_syllable_count(word_list):
    # takes a list of words and returns the average syllables per word
    temp = [syllable_count(word) for word in word_list]
    return sum(temp) / len(word_list)


def avg_sentence_length(txtstring):
    # takes a text string and returns the average words per sentence
    sentences = nltk.sent_tokenize(txtstring)
    temp = [len(str_to_words(sentence)) for sentence in sentences]
    return sum(temp) / len(sentences)


content_pos_tags = ("JJ", "NN", "RB", "VB", "FW")


def content_filter(word_list):
    # takes a word list and uses NLTK POS tagging to return a list of the content words
    tagged_word_list = nltk.tag.pos_tag(word_list)
    
    # filter the tagged list using the content_pos_tags
    content_words = [word for word, tag in tagged_word_list if tag.startswith(content_pos_tags)]
    return content_words


def lexical_density(word_list):
    # takes a word list and computes token-based lexical density
    return len(content_filter(word_list)) / len(word_list)


def flesch_reading_ease(asl, asw):
    # takes the average sentence length of a text and the average word length in syllables and returns the flesch reading ease score
    return 206.835 - (1.015 * asl) - (84.6 * asw)


def text_scoring(filepath):
    # creates a dictionary of all computed values for a given filepath
    score_dict = {'Filepath': filepath} 
    text = file_to_str(filepath)
    word_list = str_to_words(text)
    score_dict['Word count'] = len(word_list)
    score_dict['Average word length'] = avg_word_length(word_list)
    score_dict['Average syllable count'] = avg_syllable_count(word_list)
    score_dict['Average sentence length'] = avg_sentence_length(text)
    score_dict['Type-Token Ratio'] = ttr(word_list)
    score_dict['Hapax/Token Ratio'] = hapax_token_ratio(word_list)
    score_dict['Hapax/Type Ratio'] = hapax_type_ratio(word_list)
    score_dict['Lexical density'] = lexical_density(word_list)
    score_dict['Flesch Reading Ease'] = flesch_reading_ease(score_dict['Average sentence length'],score_dict['Average syllable count'])
    return score_dict


def print_results(scoring_dictionary):
    # prints out the results of a scoring dictionary from the function text_scoring()
    for label, score in scoring_dictionary.items():
        if isinstance(score, float):
            print(f"{label:<28} {score:.2f}")
        else:
            print(f"{label:<28} {score}")


def compare_results(dictionary1, dictionary2):
    # prints out the comparison results of 2 scoring dictionaries from the function text_scoring()
    filename1 = dictionary1["Filepath"].split('/')[-1]
    filename2 = dictionary2["Filepath"].split('/')[-1]
    
    # set column width and print out the table heading
    column_width = len(filename1) + 3
    print(f"{'':<28} {filename1:<{column_width}} {filename2}")
    print(" "*28, "-"*(column_width + len(filename2)+1))
    
    for label, score1, score2 in zip(dictionary1.keys(), dictionary1.values(), dictionary2.values()):
        if isinstance(score1, float):
            print(f"{label:<28} {score1:<{column_width}.2f} {score2:.2f}")
        else:
            print(f"{label:<28} {score1:<{column_width}} {score2}")


def main():
	parser = argparse.ArgumentParser(description="Analyzes lexical density, readibility, and other token/type analyses of a plaintext file. Accepts an optional second txt file for comparison.")
	parser.add_argument('file1')
	parser.add_argument('file2', nargs='?', default=None)
	args = parser.parse_args()
	
	if args.file2 is not None:
   	    compare_results(text_scoring(args.file1), text_scoring(args.file2))
	else:
   	    print_results(text_scoring(args.file1))


if __name__ == "__main__":
    main()