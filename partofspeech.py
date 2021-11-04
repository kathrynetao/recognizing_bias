#part of speech
import nltk
#nltk.download()

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
stop_words = set(stopwords.words('english'))
  

txt1 = "It was just like old times.  On Wednesday alone, Donald Trump issued pronouncements on a potential war with China, what Congress should do about the debt ceiling, false claims of a stolen election and his Fox News ally “the great Sean Hannity”.Mark Meadows, former White House chief of staff, stands behind Donald Trump on 29 July 2020.‘Can you believe this?’: key takeaways from the report on Trump’s attempt to steal the electionRead moreBut how many people noticed?Cast into the social media wilderness, the former US president releases statements by email these days, clogging the inboxes of reporters whose attention has turned elsewhere. The era when a single tweet from Trump could electrify cable news, rattle financial markets and unnerve foreign capitals is long gone." 
txt2 = "bad good, worst,  yucky banned blue, bluer, bluest"   
  
# sent_tokenize is one of instances of 
# PunktSentenceTokenizer from the nltk.tokenize.punkt module

def adjective_detector(txt):
    adj = []
    comps = []
    sups = []
        
    tokenized = sent_tokenize(txt)
    for i in tokenized:
          
        # Word tokenizers is used to find the words 
        # and punctuation in a string
        wordsList = nltk.word_tokenize(i)
      
        # removing stop words from wordList
        wordsList = [w for w in wordsList if not w in stop_words] 
      
        #  Using a Tagger. Which is part-of-speech 
        # tagger or POS-tagger. 
        tagged = nltk.pos_tag(wordsList)

        
        for i in tagged:
            if i[1] == 'JJ':
                adj.append(i[0])
            if i[1] == 'JJR':
                comps.append(i[0])
            if i[1] == 'JJS':
                sups.append(i[0])

    print ("Adjective Detected:", adj)
    print ("Comparative Detected:", comps)
    print ("Superlatives Detected:", sups)
    return tagged

adjective_detector(txt1)
adjective_detector(txt2)
      
        #print(tagged)
