from django.http import HttpResponse
from django.shortcuts import render
import operator

def home(request):
    return render(request, 'home.html')


def count(request):
    fulltext = request.GET["fulltext"]
    chars = len(fulltext)
    sentences = len(fulltext.split("."))
    edited = fulltext

    punctuation = [",", "'", "-", "!", ".", "?", ":", "(", ")", "{", "}", "[", "]", "&", "^", "/", "=", "*", "_", ";", "<", ">", '"', "—", "”", "’", "“", "...", ".."]
    limited = ["re", "are", "am", "is", "ll", "the", "that", "but", "and", "have", "has", "had", "for", "this", "who", "they", "our", "what", "which", "from", "these", "there", "not", "ago", "any", "some", "those", "their", "will", "nor", "did", "thus", "here", "with", "where", "how", "its", "while", "also", "could", "been", "into", "much", "many", "non", "should", "was", "when", "you", "me", "your", "us", "than", "him", "her", "why", "were", "then"]
    positive_file = open("word_analyser/positive_words.txt", "r").read().split()
    negative_file = open("word_analyser/negative_words.txt", "r").read().split()
    print(positive_file)
    print(negative_file)

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

    # word accumulation
    word_counts = {}
    limited_dict = {}
    for word in wordlist:
        if len(word) > 2:
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
