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
    print(html)
    # word_list = bias.bias_word_count(article)[1]
    # for word in word_list:
    #     if word in html:
    #         html = html.replace(word, '<span class = "bias_words">' + word + '</span>')
    # print(html)

    # data, number = bias.get_article(inputText)
    # found_reg_list, index_list = ne.number_extract(data)
    # count = 0
    # for i in index_list:
    #   data = data[0: i[0] + count * 31] + '<span class = "numbers">' + data[i[0] + count * 31:i[1]+ count * 31] + '</span>' + data[i[1]+ count * 31:]
    #   count += 1

    # resText = Markup(html)
    # print(resText)
    return render_template('index.html', input_text = inputText, res_text = html)

if __name__ == '__main__':
    app.run()
