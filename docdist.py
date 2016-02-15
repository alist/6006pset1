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

    magsSquared = [0.0]*len(lists)
    dot = 0.0
    for freq in frequencies.itervalues():
        magsSquared = map(lambda x, y: x + pow(y, 2), magsSquared, freq)
        dot = dot + reduce(lambda x, y: x * y, freq)

    mags = map(math.sqrt, magsSquared)
    denominator = reduce(lambda x, y: x * y, mags)
    cosign = dot / denominator

    radians = math.acos(cosign)
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
    # so the same approach as doc_dist, except when lists are iterated through, we insert "\(words[i]) \(words[i+1])"
    return 1

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
    # we could store
    return 0
