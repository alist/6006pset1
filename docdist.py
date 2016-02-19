#!/usr/bin/python

import string
import sys
import math
    # math.acos(x) is the arccosine of x.
    # math.sqrt(x) is the square root of x.

# global variables needed for fast parsing
# translation table maps upper case to lower case and punctuation to spaces
translation_table = string.maketrans(string.punctuation+string.uppercase[0:26],
                                     " "*len(string.punctuation)+string.lowercase[0:26])

def extract_words(filename):
    """
    Return a list of words from a file
    """
    try:
        f = open(filename, 'r')
        doc = f.read()
        lines = doc.translate(translation_table)
        return lines.split()
    except IOError:
        print "Error opening or reading input file: ",filename
        sys.exit()

##############################################
## Part a. Count the frequency of each word ##
##############################################
def doc_dist(word_list1, word_list2):
    """
    Returns a float representing the document distance
    in radians between two files when given the list of
    words from both files
    """
    #pylint: disable=W0110,W0141
    #I store lists [doc 1, doc2] at each dictionary location
    #I cosign the whole dictionary by iterating through values
    frequencies = {"emptyexample" : [0, 0]}
    lists = [word_list1, word_list2]
    for ai, alist in enumerate(lists):
        for word in alist:
            #addition array for particular word
            addArray = [0]*(len(lists))
            addArray[ai] = 1
            frequencies[word] = addArray if word not in frequencies else \
                map(lambda a, b: a + (b if b is not None else 0), addArray, frequencies[word])

    radians = dotProduct(frequencies)
    return radians

##############################################
## Part b. Count the frequency of each pair ##
##############################################
def doc_dist_pairs(word_list1, word_list2):
    """
    Returns a float representing the document distance
    in radians between two files based on unique
    consecutive pairs of words when given the list of
    words from both files
    """
    #pylint: disable=W0110,W0141
    # The same approach as doc_dist, except when lists are iterated through
    #       I insert "\(words[i]) \(words[i+1])"
    frequencies = {"emptyexample" : [0, 0]}
    lists = [word_list1, word_list2]
    for ai, alist in enumerate(lists):
        for i, word in enumerate(alist):
            if i >= len(alist) -2: break
            addArray = [0]*(len(lists))
            addArray[ai] = 1
            wordpair = "{0} {1}".format(word, alist[i+1])
            frequencies[wordpair] = \
                addArray if wordpair not in frequencies else \
                map(lambda a, b: a + (b if b is not None else 0), addArray, frequencies[wordpair])

    radians = dotProduct(frequencies)
    return radians


def dotProduct(frequencies):
    magsSquared = [0.0]*2
    dot = 0.0
    for freq in frequencies.itervalues():
        magsSquared = map(lambda x, y: x + pow(y, 2), magsSquared, freq)
        dot = dot + reduce(lambda x, y: x * y, freq)

    mags = map(math.sqrt, magsSquared)
    denominator = reduce(lambda x, y: x * y, mags)
    cosign = dot / denominator

    radians = math.acos(cosign)
    return radians

#############################################################
## Part c. Count the frequency of the 50 most common words ##
#############################################################
def doc_dist_50(word_list1, word_list2):
    """
    Returns a float representing the document distance
    in radians between two files based on the
    50 most common unique words when given the list of
    words from both files
    """
    #pylint: disable=W0110,W0141
    # 1. get the frequency of the words for each list
    lists = [word_list1, word_list2]
    frequencyLists = [{"emptyexample" : 0} for _ in range(len(lists))]
    for li, alist in enumerate(lists):
        for word in alist:
            frequencyLists[li][word] = 1 if word not in frequencyLists[li] else \
                1 + frequencyLists[li][word]

    # 2. Sort lists of words by frequency
    sortedFrquencyLists = [[] for _ in range(len(lists))]
    # TODO Why do I need an alist2 here? If it's alist, it gives me "using possibly undefined loop variable"
    alist2=None
    for li, alist2 in enumerate(frequencyLists):
        sortedFrquencyLists[li] = sorted(alist2, lambda left, right: \
            cmp(left, right) if alist2[left] == alist2[right] else 1 if alist2[left] > alist2[right] else -1, reverse=True)

    # 3. Truncate sorted word lists to 50 words per list
    trimmedLists = map(lambda alist: alist[:50], sortedFrquencyLists)

    # 4. Create a new dictionary to maps words to array containing the word's count for each word list
        # 4i. Iterate through each truncated word list
        # 4ii. Iterate through each word in truncated word list
        # 4iii. Add frequency of word to the dictionary entry for the word, at the column for the current iterating list
    frequencies = {"emptyexample" : [0, 0]}
    for ai, alist in enumerate(trimmedLists):
        for word in alist:
            #addition array for particular word
            addArray = [0]*(len(lists))
            addArray[ai] = frequencyLists[ai][word] if word in frequencyLists[ai] else 0
            frequencies[word] = addArray if word not in frequencies else \
                map(lambda a, b: a + (b if b is not None else 0), addArray, frequencies[word])

    # 5. Note that the dictionary has more than 50 elements.

    # 6. Get dot-product over dictionary's frequency values for each word. The same as in my passing (b) and (a), but on reduced data.
    radians = dotProduct(frequencies)
    # output:
    # 0.423977014818
    # 0.963287391907
    # 0.871419668472
    return radians
