from django.shortcuts import render
import operator
import requests
import re
from bs4 import BeautifulSoup

# html cleaner
def cleanhtml(raw_html):
    cleanr = re.compile('<body.*?>(.*)</body>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext



def home(request):
    return render(request, 'home.html')


def count(request):

    # get the text from link or text area
    try:
        linktext = request.GET["linktext"]
        response = requests.get(linktext)
        text = cleanhtml(response.text)
        soup = BeautifulSoup(text, 'html.parser')
        fulltext = soup.get_text()
        fulltext = fulltext.strip()
        fulltext = fulltext.replace("\n", " ")
    except:
        fulltext = request.GET["fulltext"]



    # define some variables for counter
    chars = len(fulltext)
    sentences = len(fulltext.split("."))
    edited = fulltext


    # define the punctuation characters and limited words
    punctuation = [",", "'", "-", "!", ".", "?", ":", "(", ")", "{", "}", "[", "]", "&", "^", "/", "=", "*",
                "_", ";", "<", ">", '"', "—", "”", "’", "“", "...", "..", "‘"]
    limited = ["re", "are", "am", "is", "ll", "the", "that", "but", "and", "have", "has", "had", "for", "this", "who", "they", "our", "what", "which", "would",
            "from", "these", "there", "not", "ago", "any", "some", "those", "their", "will", "nor", "did", "thus", "here", "with", "where", "how", "its", "while",
            "also", "could", "been", "into", "much", "many", "non", "should", "was", "when", "you", "me", "your", "us", "than", "him", "her", "why", "were", "then"]

    # get positive and negative words
    positive_file = open("word_analyser/positive_words.txt", "r").read().split()
    negative_file = open("word_analyser/negative_words.txt", "r").read().split()

    # remove punctuations
    for char in edited:
        if char in punctuation:
            edited = edited.replace(char, " ")

    # make a list from word
    wordlist = edited.split()

    # positive and negatives words
    positives = 0
    negatives = 0
    neutral = 0

    for word in wordlist:
        if word in positive_file:
            positives += 1
        elif word in negative_file:
            negatives += 1
        else:
            neutral += 1

    # word counter
    word_counts = {}
    limited_dict = {}

    for word in wordlist:
        if len(word) > 2 and len(word) < 20:
            if word.lower() not in limited:
                if word.lower() in word_counts:
                    word_counts[word.lower()] += 1
                else:
                    word_counts[word.lower()] = 1
            else:
                if word.lower() in limited_dict:
                    limited_dict[word.lower()] += 1
                else:
                    limited_dict[word.lower()] = 1


    limited_words = len(limited_dict)
    sortedwords = sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)
    return render(request, 'count.html', {"fulltext": fulltext, "count": len(wordlist), "word_counts": sortedwords, "characters": chars, "sentences": sentences, "limited": limited_words, "positives": positives, "negatives": negatives, "neutral": neutral} )




def about(request):
    return render(request, 'about.html')
