import nltk
import ssl
import re
import requests

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
# nltk.download('punkt')

from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from textblob import TextBlob
from goose3 import Goose
from requests import get

from newspaper import Article
from newspaper import fulltext



#reading the url from txt file & creating a string
text_file = open("article.txt", "r")
url = text_file.read()
text_file.close()
print(url)


response = get(url)
print(response)
extractor = Goose()
article = extractor.extract(raw_html=response.content)
# print(article)
text = article.cleaned_text
print(text)



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

#     "emerg": 0, "serious": 0, "refus": 0, "crucial": 0, "high-stak": 0, "tirad": 0, "landmark": 0, "latest in a string of": 0, "major": 0, "turn up the heat": 0, "critic": 0, "decri": 0, "offens": 0, "stern talk": 0, "facing calls to": 0, "meaning": 0, "even though": 0, "monument": 0, "signific": 0,
#     "final": 0, "surfac": 0, "acknowledg": 0, "refusing to say": 0, "conced": 0, "dodg": 0, "admiss": 0, "came to light": 0, "admit to": 0, "mock": 0, "rage": 0, "brag": 0 , "fume": 0, "lashed out": 0, "incens": 0, "scof": 0, "frustrat": 0, "erupt": 0, "rant": 0, "boast": 0, "gloat": 0,
#     "good": 0, "better": 0, "best": 0, "is considered to b": 0, "seem": 0, "extrem": 0, "may mean that": 0, "could": 0, "appar": 0, "bad": 0, "wors": 0, "worst": 0, "it's likely that": 0, "danger": 0, "suggest": 0, "would seem": 0, "decri": 0, "possibl": 0,
#     "shock": 0, "remark": 0, "rip": 0, "chaotic": 0, "lashed out": 0, "onslaught": 0, "scath": 0, "showdown": 0, "explos": 0, "slam": 0, "forc": 0, "warn": 0, "embroiled in": 0, "torrent of tweet": 0, "desper": 0
# }

#adds words into stemmed dict
def stemmer_dict(lst):
    for word in lst:
        word = word.lower()
        x = snow.stem(word)
        if x not in stemmed_bias_words:
            stemmed_bias_words[x] = 0

    return stemmed_bias_words

print(stemmer_dict(bias_word_lst))

#gets sentiment analysis
def sentiment_analysis(str):
    testimonial = TextBlob(str)
    return testimonial.sentiment
print(sentiment_analysis(data))

#strips punctuation
def __strip(str):
    res = re.sub(r'[^\w\s]', '', str)
    res.casefold()
    return res

#counting bias terms in the article
def bias_word_count(str):
    stemmed_bias_words = stemmer_dict(bias_word_lst)
    counter = 0
    bias_word_count = []
    str = __strip(str)
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

    print(stemmed_bias_words)
    return [counter, bias_word_count]

print(bias_word_count(data))

#finding a final score based off of our theory
# def main(str):
#     subj = sentiment_analysis(str).subjectivity
#     biased_words = bias_word_count(str)[0]
#     x = ((biased_words/len(data)))
#     print(biased_words)
#     print(sentiment_analysis(str))


# main(data)


# def part_of_speech(str):
