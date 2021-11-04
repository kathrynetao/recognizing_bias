import nltk
import ssl
import re
import requests
import number_extractor

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from textblob import TextBlob
from goose3 import Goose
from requests import get

url = "https://www.cbc.ca/news/business/air-canada-vaccine-suspensions-1.6235222"


#reading the url from txt file & creating a string
# text_file = open("article.txt", "r")
# link = text_file.read()
# text_file.close()
# print(link)


response = get(url)
extractor = Goose()
article = extractor.extract(raw_html=response.content)
# print(article)
data = article.cleaned_text
print(data)
number = number_extractor.number_extract(data)

#creating the stemmer
snow = SnowballStemmer(language='english')

#word list of terms that indicate bias
bias_word_lst = ["Emerge", "Serious", "Refuse", "Crucial", "High-stakes", "Tirade", "Landmark", "Latest in a string of", "Major", "Turn up the heat", "Critical", "Decrying", "Offend", "Stern talks", "Offensive", "Facing calls to", "Meaningful", "Even though", "Monumental", "Significant",
"Finally", "Surfaced", "Acknowledged", "Emerged", "Refusing to say", "Conceded", "Dodged", "Admission", "Came to light", "Admit to", "Mocked", "Raged", "Bragged", "Fumed", "Lashed out", "Incensed", "Scoffed", "Frustration", "Erupted", "Rant", "Boasted", "Gloated",
"Good", "Better", "Best", "Is considered to be", "Seemingly", "Extreme", "May mean that", "Could", "Apparently", "Bad", "Worse", "Worst", "It's likely that", "Dangerous", "Suggests", "Would seem", "Decrying", "Possibly",
"Shocking", "Remarkable", "Rips", "Chaotic", "Lashed out", "Onslaught", "Scathing", "Showdown", "Explosive", "Slams", "Forcing", "Warning", "Embroiled in", "Torrent of tweets", "Desperate","Law and Order", "States Rights", "Urban", "Inner-City", "Welfare", "Moochers", "Takers",
"Looters", "Tax Cuts", "Minimum Wage", "War on Drugs", "War on Crime", "Tough on Crime", "Super Predators", "Rioters", "Special Interests", "Big Government", "thug", "terrorist", "elite", "Black-on-black crime", "Bossy", "sassy", "uppity", "radical", "raid", "loot", "riot",]

#stemmed words that indicated bias
stemmed_bias_words = {}

#adds words into stemmed dict
def stemmer_dict(lst):
    for word in lst:
        word = word.lower()
        x = snow.stem(word)
        if x not in stemmed_bias_words:
            stemmed_bias_words[x] = 0

    return stemmed_bias_words

# print(stemmer_dict(bias_word_lst))

#gets sentiment analysis
def sentiment_analysis(str):
    testimonial = TextBlob(str)
    return testimonial.sentiment
print(sentiment_analysis(data))

#strips punctuation
def __strip(str):
    # parsed = str.split('"')
    # print(parsed)
    # length = len(parsed)
    # print(length)
    res = re.sub(r'[^\w\s]', '', str)
    res.casefold()
    return res

#counting bias terms in the article
def bias_word_count(str):
    stemmed_bias_words = stemmer_dict(bias_word_lst)
    counter = 0
    bias_word_count = []
    str = __strip(str)
    print(str)
    token_words = word_tokenize(str)
    stem_sentence = []
    for word in token_words:
        stem_sentence.append(snow.stem(word))

    for word in stem_sentence:
        if word in stemmed_bias_words:
            stemmed_bias_words[word] += 1
            counter += 1
            if word not in bias_word_count:
                bias_word_count.append(word)

    return [counter, bias_word_count]

print(bias_word_count(data))
print(number)
#finding a final score based off of our theory
# def main(str):
#     subj = sentiment_analysis(str).subjectivity
#     biased_words = bias_word_count(str)[0]
#     x = ((biased_words/len(data)))
#     print(biased_words)
#     print(sentiment_analysis(str))


# main(data)


# def part_of_speech(str):
