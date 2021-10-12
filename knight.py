import json
import pandas as pd
from textblob import TextBlob

from textblob import TextBlob
x = TextBlob("hello I like you so much").sentiment
print(x)


def emote():
    s = input("Enter a sentence!")
    x = TextBlob(s).sentiment
    print(x)

while True:
    emote()
