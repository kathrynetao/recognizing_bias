import os
import bias
import number_extractor as ne
from flask import Flask, request, render_template, Markup
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def demo():
  if request.method == 'GET':
    return render_template('index.html', input_text = '', res_text = '')
  else:
    inputText = request.form.get("input_text")
    html = bias.get_html(inputText)
    article = bias.get_article(inputText)
    base_url = 'https://' + bias.base_url(inputText)
    html = html.decode("utf-8")
    if 'href="/' in html:
        html = html.replace('href="/', 'href="' + base_url + '/')

    htmlnum = ne.highlight_number(html, article)
    htmlword = bias.highlight_word_bank(html, article)
    htmlquotes = bias.highlight_quotes(html,article)
    htmladj = bias.highlight_adjectives(html, article)

    html = ne.highlight_number(html, article)
    html = bias.highlight_word_bank(html, article)
    html = bias.highlight_quotes(html,article)
    html = bias.highlight_adjectives(html, article)

    resText = Markup(html)
    resTextnum = Markup(htmlnum)
    resTextword = Markup(htmlword)
    resTextquotes = Markup(htmlquotes)
    resTextadj = Markup(htmladj)

    questions_main = "\nWhose point of view is the article representing? Private/public/national/international?\n\nAre there any assumptions/stereotypes/widely-held beliefs (within the context of the article) that the article refers to?"
    questions_num = "\nWhat is the context of these numbers?\nCan you find the original source of data?\n\nWho funds the research behind the data?\nIs the research (and relevant data) representative of and relevant to the context?"
    questions_word = "\nWhat is the context behind these words?\nDo they evoke certain emotions when read?\n\nDo they make you as the reader think or feel differently about the topic?\n\nIs the language that is described and used respectful towards people?"
    questions_adj = "\nHow many extreme adjectives are there (in purple)?\n\nAre the adjectives they are using relevant to what they modify?\n\nIs the language loaded? Consider recent events that relate to the context of the article and how they may affect the meanings of words/phrases."
    questions_quotes = "\nAre they official sources? Civilian sources? Eyewitness? Experts in the field?\n\nAre there any potential conflicts of interest? This might be subtle, but consider the backgrounds of people being interviewed. Are people representative of the community/context they are commenting on? "
    return render_template('index.html', input_text = inputText, res_text = resText, res_text_num = resTextnum, res_text_words = resTextword, res_text_quotes = resTextquotes, res_text_adj = resTextadj, questions_main = questions_main, questions_num = questions_num, questions_word = questions_word, questions_adj = questions_adj, questions_quotes = questions_quotes )

@app.route("/number/", methods=['GET', 'POST'])
def display_number():

    inputText = request.form.get("input_text")
    html = bias.get_html(inputText)
    article = bias.get_article(inputText)
    base_url = 'https://' + bias.base_url(inputText)
    html = html.decode("utf-8")
    if 'href="/' in html:
        html = html.replace('href="/', 'href="' + base_url + '/')

    html = ne.highlight_number(html, article)

    resText = Markup(html)
    return render_template('index.html', input_text = inputText, res_text = resText)

if __name__ == '__main__':
    app.run()
