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
        html = bias.get_html(inputText)
        base_url = 'https://' + bias.base_url(inputText)
        html = html.decode("utf-8")
        if 'href="/' in html:
            html = html.replace('href="/', 'href="' + base_url + '/')

        data= bias.get_article(inputText)
        found_reg_list, index_list = ne.number_extract(data)
        count = 0
        for i in index_list:
          data = data[0: i[0] + count * 31] + '<span class = "numbers">' + data[i[0] + count * 31:i[1]+ count * 31] + '</span>' + data[i[1]+ count * 31:]
          count += 1

        resText = Markup(html)

        return render_template('index.html', input_text = inputText,res_text = resText)
    # inputText = urllib.parse.quote_plus(inputText)
    # return redirect(url_for('news',restext = inputText))

# @app.route('/news/<restext>')
# def news(restext):
#     restext = urllib.parse.unquote(restext)
#     html = bias.get_html(restext)
#     base_url = 'https://' + bias.base_url(restext)
#     html = html.decode("utf-8")
#     if 'href="/' in html:
#         html = html.replace('href="/', 'href="' + base_url + '/')
#
#     data= bias.get_article(restext)
#     found_reg_list, index_list = ne.number_extract(data)
#     count = 0
#     for i in index_list:
#       data = data[0: i[0] + count * 31] + '<span class = "numbers">' + data[i[0] + count * 31:i[1]+ count * 31] + '</span>' + data[i[1]+ count * 31:]
#       count += 1
#
#     resText = Markup(html)
#     return render_template('news.html',res_text = resText)

if __name__ == '__main__':
    app.run()