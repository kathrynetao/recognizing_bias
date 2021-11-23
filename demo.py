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
    print(base_url)
    html = html.decode("utf-8")
    if 'href="/' in html:
        html = html.replace('href="/', 'href="' + base_url + '/')

    word_list = bias.bias_word_count(article)[1]
    print(word_list)
    for word in word_list:
        if word in html:
            html = html.replace(word, '<span class = "bias_words">' + word + '</span>')

    resText = Markup(html)
    return render_template('index.html', input_text = inputText, res_text = resText)

if __name__ == '__main__':
    app.run()
