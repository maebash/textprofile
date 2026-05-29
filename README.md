# Text Profile

A python tool that produces a quick overview of various basic corpus linguistics/NLP metrics of a single text, including Type-Token Ratio and Hapax legomena/Token Ratio, as well as some more widely useful analyses, such as average word and sentence length, syllable count, and Flesch Reading Ease. It can also be used to compare two text files. 

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
	- [Averages](#averages)
	- [Syllable Count](#syllable-count)
	- [_Hapax legomena_ and Type-Token Ratios](#ratios)
	- [Lexical Density](#lexical-density)
	- [Flesch Reading Ease](#flesch-reading-ease)
- [License](#license)

## Description

Text Profile computes the following values for a text file:

- Word Count
- Average word length (in characters)
- Average syllable count (per word)
- Average sentence length (in words)
- Type-token Ratio
- _Hapax legomena_/Token Ratio
- _Hapax legomena_/Type Ratio
- Lexical Density
- Flesch Reading Ease

When two text files are input, it will display a table with the values for both text files side-by-side for comparison.

This tool is an experiment in manually computing these values, instead of using preexisting libraries like `textstat`. Please see the **Features** section below to read more about how some of the values were computed, and the limitations of some of these computations.

It is limited to plaintext files in English, and results for certain values, like syllable count, reflect North American English pronunciation. Some of the tools used, such as NLTK's POS tagger and the CMU dict are English specific, and the tool currently doesn't support texts with non-English characters. 

All numerals and punctuation are excluded from calculations, and the tool assumes an input of a clean plaintext file with no headers or titles.

## Installation

### Dependencies

TxtProfile is written in Python, and requires the Natural Language Toolkit (NLTK) library. 

```
pip install nltk
```

There are also three additional nltk packages needed.

```
python -m nltk.downloader punkt_tab cmudict averaged_perceptron_tagger_eng
```

### Installing

Clone the repo or download the files

```
git clone https://github.com/maebash/textprofile
```

## Usage

To run, call the python script and pass either one or two .txt files. 

```
python textprofile.py sampletexts/afarewelltoarms.txt
```

If a single file is called as an argument, the results appear as such:

```
Filepath                     sampletexts/afarewelltoarms.txt
Word count                   89057
Average word length          3.95
Average syllable count       1.26
Average sentence length      12.55
Type-Token Ratio             0.06
Hapax/Token Ratio            0.02
Hapax/Type Ratio             0.43
Lexical density              0.57
Flesch Reading Ease          87.47
```

Optionally, two files can be passed through the script.

```
python textprofile.py sampletexts/afarewelltoarms.txt sampletexts/thegreatgatsby.txt
```

With 2 text inputs, the result output is given a table format. The script will identify the name of the text file, and adjust the column sizes accordingly. 

```
                             afarewelltoarms.txt    thegreatgatsby.txt
                             -----------------------------------------
Filepath                     sampletexts/afarewelltoarms.txt sampletexts/thegreatgatsby.txt
Word count                   89057                  48661
Average word length          3.95                   4.27
Average syllable count       1.26                   1.37
Average sentence length      12.55                  19.83
Type-Token Ratio             0.06                   0.12
Hapax/Token Ratio            0.02                   0.06
Hapax/Type Ratio             0.43                   0.53
Lexical density              0.57                   0.57
Flesch Reading Ease          87.47                  70.45
```


## Features

### Averages

Text Profile computes the **average word length** and **average sentence length** of a text.

NLTK's sentence tokenizer tool is used to extract each sentence from the .txt, and average sentence length is computed by calculating the average length of every sentence in words. 

A regex is used to extract a list of all words (contractions are counted as a single token). Average word length is computed by calculating the average length of every word in the text in characters (includes apostrophes). This was used instead of NLTK's word tokenizer to preserve contractions.

### Syllable Count 

To compute the average syllable count, the CMU Pronouncing Dictionary is primarily used to count the number of syllables per word. 

For any word in the CMU dictionary, the output is a list of phones in that word, as pronounced in General North American English. Each vowel phone is marked with a number to denote stress. 

For example, the word `dictionary` /ˈdɪk.ʃəˌnɛ.ɹi/ in CMU outputs the following:

``` 
cmudict.dict()["dictionary"] = ["D", "IH1", "K", "SH", "AH0", "N", "EH2", "R", "IY0"]
```

The primary stress is on the first syllable, /dɪk/, noted with the number 1, and the secondary stress is on the third syllable, /nɛ/, noted by the number 2. The other two syllables have no stress, noted by the number 0.

The syllable counter in this tool counts the number of phones with marked stress for a given word, which should match the number of syllables. Some words have multiple pronunciations in the CMU Pronouncing Dictionary, in which case the first pronunciation is used.

For words that are not in the CMU Pronouncing Dictionary, a fallback method was used that counts the number of vowel clusters in a word. This will accurately count most words, except for when there are multi-syllable vowel clusters, vocalic ys, and silent vowels. For example, `cake` would be counted as having 2 syllables, and `shyly` as having 0. 

As a final fallback, words that are not in the CMU dictionary and do not have a vowel `aeiou` are counted as having 1 syllable. This would catch monosyllabic words like `crypt`, but also longer words like `shyly`.

Given that the CMU Pronouncing Dictionary contains over 130k words (including cake, crypt, and shyly), slight miscalculated syllable counts should not skew the data massively, except in shorter texts with specialized language. 

### Ratios

The Type-Token Ratio (TTR) is computed using the length of the list of words (tokens) and the length of a word frequency dictionary (types) for that same list. 

A _hapax legomenon_ is a word that occurs only once in its context. Text Profile computes two metrics related to the _hapax legomena_ of a text: the _hapax_ to token ratio, and the _hapax_ to type ratio.

### Lexical Density

Text Profile computes Lexical Density by using NLTK's part of speech tagging to filter the list of tokens to only the content words. 

NLTK's `pos_tag` by default uses the Penn Treebank tagset. TxtProfile finds lexical tokens (content words) by searching for words with tags that begin with `('JJ', 'NN', 'RB', 'VB', 'FW')`. These are adjectives, nouns, adverbs, verbs, and "foreign words". 

Text Profile uses the number of lexical tokens and divides by total tokens to get the lexical density rating. In some calculations of Lexical Density, this ratio is multiplied by 100, but Text Profile leaves the ratio as is. 

### Flesch Reading Ease

Flesch Reading Ease is calculated using previously computed averages. 

The following formula is used to calculate the reading ease.

```
FRE = 206.835 - (1.015 * Average Sentence Length) - (84.6 * Average Syllables per Word)
```

Scores close to 100 represent texts that are the 'easiest' to read, whereas scores below 50 represent supposed college-level texts, and scores below 10 represent texts that are extremely difficult to read. 

Because syllables per word has a massive impact on the computed reading ease and the syllable counter is not perfect, the Flesch Reading Ease scores are likely to be affected. This is especially true for shorter inputs, as well as those with specialized language and/or many contractions that may not be in the CMU dictionary. Overcounting of syllables will result in lower reading ease scores than is accurate, and undercounting will result in higher than accurate ease. 

## License

[MIT](https://choosealicense.com/licenses/mit/)