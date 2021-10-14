import nltk
import ssl
import re
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

#reading the article from txt file
text_file = open("article.txt", "r")
data = text_file.read()
text_file.close()
print(data)

#creating the stemmer
snow = SnowballStemmer(language='english')

bias_word_lst = ["Emerge", "Serious", "Refuse", "Crucial", "High-stakes", "Tirade", "Landmark", "Latest in a string of", "Major", "Turn up the heat", "Critical", "Decrying", "Offend", "Stern talks", "Offensive", "Facing calls to", "Meaningful", "Even though", "Monumental", "Significant",
"Finally", "Surfaced", "Acknowledged", "Emerged", "Refusing to say", "Conceded", "Dodged", "Admission", "Came to light", "Admit to", "Mocked", "Raged", "Bragged", "Fumed", "Lashed out", "Incensed", "Scoffed", "Frustration", "Erupted", "Rant", "Boasted", "Gloated",
"Good", "Better", "Best", "Is considered to be", "Seemingly", "Extreme", "May mean that", "Could", "Apparently", "Bad", "Worse", "Worst", "It's likely that", "Dangerous", "Suggests", "Would seem", "Decrying", "Possibly",
"Shocking", "Remarkable", "Rips", "Chaotic", "Lashed out", "Onslaught", "Scathing", "Showdown", "Explosive", "Slams", "Forcing", "Warning", "Embroiled in", "Torrent of tweets", "Desperate"]

stemmed_bias_words = {
    "emerg": 0, "serious": 0, "refus": 0, "crucial": 0, "high-stak": 0, "tirad": 0, "landmark": 0, "latest in a string of": 0, "major": 0, "turn up the heat": 0, "critic": 0, "decri": 0, "offens": 0, "stern talk": 0, "facing calls to": 0, "meaning": 0, "even though": 0, "monument": 0, "signific": 0,
    "final": 0, "surfac": 0, "acknowledg": 0, "emerg": 0, "refusing to say": 0, "conced": 0, "dodg": 0, "admiss": 0, "came to light": 0, "admit to": 0,
    "mock": 0, "rage": 0, "brag": 0 , "fume": 0, "lashed out": 0, "incens": 0, "scof": 0, "frustrat": 0, "erupt": 0, "rant": 0, "boast": 0, "gloat": 0,
    "good": 0, "better": 0, "best": 0, "is considered to b": 0, "seem": 0, "extrem": 0, "may mean that": 0, "could": 0, "appar": 0, "bad": 0, "wors": 0, "worst": 0, "it's likely that": 0, "danger": 0, "suggest": 0, "would seem": 0, "decri": 0, "possibl": 0,
    "shock": 0, "remark": 0, "rip": 0, "chaotic": 0, "lashed out": 0, "onslaught": 0, "scath": 0, "showdown": 0, "explos": 0, "slam": 0, "forc": 0, "warn": 0, "embroiled in": 0, "torrent of tweet": 0, "desper": 0
}


def sentiment_analysis(str):
    testimonial = TextBlob(str)
    return testimonial.sentiment

# sentiment_analysis(data)
#
# # def most_frequent(str):
#
def __strip(str):
    res = re.sub(r'[^\w\s]', '', str)
    res.casefold()
    return res


def bias_word_count(str):
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
            bias_word_count.append(word)
    return [counter, bias_word_count]


# bias_word_count(data)

def main(str):
    subj = sentiment_analysis(str).subjectivity
    biased_words = bias_word_count(str)[0]
    bias_percentage = (((biased_words/len(bias_word_lst)) + subj) / 2) * 100
    print("This article is: ")
    print(bias_percentage, "% biased")



main(data)


# def part_of_speech(str):
