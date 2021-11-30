import nltk
import ssl
import re
import requests
import number_extractor
import partofspeech

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

url = "https://www.vox.com/2016/7/25/12270880/donald-trump-racist-racism-history"

#creating the stemmer
snow = SnowballStemmer(language='english')

#word list of terms that indicate bias
bias_word_lst = ["Emerge", "Serious", "Refuse", "Crucial", "High-stakes", "Tirade", "Landmark", "Latest in a string of", "Major", "Turn up the heat", "Critical", "Decrying", "Offend", "Stern talks", "Offensive", "Facing calls to", "Meaningful", "Even though", "Monumental", "Significant",
"Finally", "Surfaced", "Acknowledged", "Emerged", "Refusing to say", "Conceded", "Dodged", "Admission", "Came to light", "Admit to", "Mocked", "Raged", "Bragged", "Fumed", "Lashed out", "Incensed", "Scoffed", "Frustration", "Erupted", "Rant", "Boasted", "Gloated",
"Good", "Better", "Best", "Is considered to be", "Seemingly", "Extreme", "May mean that", "Could", "Apparently", "Bad", "Worse", "Worst", "It's likely that", "Dangerous", "Suggests", "Would seem", "Decrying", "Possibly",
"Shocking", "Remarkable", "Rips", "Chaotic", "Lashed out", "Onslaught", "Scathing", "Showdown", "Explosive", "Slams", "Forcing", "Warning", "Embroiled in", "Torrent of tweets", "Desperate","Law and Order", "States Rights", "Urban", "Inner-City", "Welfare", "Moochers", "Takers",
"Looters", "Tax Cuts", "Minimum Wage", "War on Drugs", "War on Crime", "Tough on Crime", "Super Predators", "Rioters", "Special Interests", "Big Government", "thug", "terrorist", "elite", "Black-on-black crime", "Bossy", "sassy", "uppity", "radical", "raid", "loot", "riot", "Abandon", "Abuse", "Acknowledged", "Admission", "Admit to", "Afraid", "Alone", "Anger", "Annoy", "Apparently", "Ashamed", "Attack", "Avoid", "Awful", "Bad", "Beg", "Blame", "Boasted", "Bore", "Bragged", "Broken", "Came to light", "Cannot", "Chaotic", "Cheat", "Clumsy", "Conceded", "Confuse", "Critical", "Crucial", "Damage", "Danger", "Dangerous", "Dead", "Decrying", "Defeat", "Delay", "Deny", "Depress", "Desperate", "Difficult", "Dirty", "Disaster", "Disease", "Dishonest", "Dislike", "Dodged", "Dreadful", "Drug", "Dumb", "Embarrass", "Embroiled in", "Emerge", "Emerged", "Enemy", "Erupted", "Even though", "Evil", "Excuse", "Explosive", "Extreme", "Fail", "Failure", "False", "Fault", "Fear", "Fight", "Finally", "Force", "Forcing", "Foul", "Fright", "Frustration", "Fumed", "Furious", "Gloated", "Gossip", "Greed", "Guilty", "Harm", "Harmful", "Hate", "Hide", "Horrible", "Humiliate", "Hunger", "Hurt", "Ignore", "Ill", "Impossible", "Incensed", "Inferior", "Insane", "Insecure", "Insult", "Jealous", "Kill", "Lie", "Lost", "Miser", "Mocked", "Monumental", "Offend", "Offensive", "Onslaught", "Pain", "Pessimist", "Poison", "Poor", "Possibly", "Problem", "Quit", "Raged", "Rant", "Refuse", "Reject", "Revenge", "Rips", "Rude", "Sad", "Scathing", "Scoffed", "Shocking", "Slams", "Sorrow", "Sorry", "Steal", "Suspect", "Suspicious", "Tension", "Tirade", "Traitor", "Ugly", "Unfair", "Unfavourable", "Unhappy", "Unhealthy", "Unjust", "Unloved", "Unpleasant", "Unwanted", "Upset", "War", "Warning", "Worse", "Worst", "Worthless"
]

def get_html(url):
    response = get(url)
    extractor = Goose()
    return response.content
get_html(url)

def get_article(url):
    response = get(url)
    extractor = Goose()
    article = extractor.extract(raw_html=response.content)
    data = article.cleaned_text
    # print(data)
    number = number_extractor.number_extract(data)
    return data

data = get_article(url)


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

#gets quotes
def find_quotes(str):
    str = str.replace('“','"').replace('”','"')
    return re.findall('"([^"]*)"', str)

print(find_quotes(data))

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
        stem_sentence.append([snow.stem(word), word])

    for word in stem_sentence:
        if word[0] in stemmed_bias_words:
            stemmed_bias_words[word[0]] += 1
            counter += 1
            if word[1] not in bias_word_count:
                bias_word_count.append(word[1])
    return [counter, bias_word_count]

print(bias_word_count(data))

def base_url(url):
    base_url = url.split('/')[2]
    return base_url

#highlights words bank
def highlight_word_bank(html, article):
    word_list = bias_word_count(article)[1]
    for word in word_list:
        if word in html:
            html = html.replace(word, '<span class = "bias_words">' + word + '</span>')
    return html

def highlight_quotes(html, article):
    quotes = find_quotes(article)
    html = html.replace('“','"').replace('”','"')
    for quote in quotes:
        quote = '"' + quote + '"'
        if quote in html:
            html = html.replace(quote, '<span class = "quotes">' + quote + '</span>')

    return html

def highlight_adjectives(html, article):
    adjectives = partofspeech.adjective_detector(article)
    for type in adjectives:
        for word in adjectives[type]:
            word = " " + word + " "
            if word in html:
                html = html.replace(word, '<span class = "' + type + '">' + word + '</span>')

    return html
