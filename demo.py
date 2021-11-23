import os
import bias
import number_extractor as ne
import urllib.parse
from flask import Flask, request, render_template, Markup,redirect, url_for
app = Flask(__name__,template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html', input_text = '', res_text = '')
  else:
    inputText = request.form.get("input_text")
    # return render_template('index.html', input_text = inputText)
    inputText = urllib.parse.quote_plus(inputText)

    return redirect(url_for('news',restext = inputText))

@app.route('/news/<restext>')
def news(restext):
    restext = urllib.parse.unquote(restext)
    data, number = bias.get_article(restext)
    found_reg_list, index_list = ne.number_extract(data)
    count = 0
    for i in index_list:
      data = data[0: i[0] + count * 31] + '<span class = "numbers">' + data[i[0] + count * 31:i[1]+ count * 31] + '</span>' + data[i[1]+ count * 31:]
      count += 1

    resText = Markup(data)
    return render_template('news.html',res_text = resText)

if __name__ == '__main__':
    app.run()