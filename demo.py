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
    data, number = bias.get_article(inputText)
    found_reg_list, index_list = ne.number_extract(data)
    count = 0
    for i in index_list:
      data = data[0: i[0] + count * 31] + '<span class = "numbers">' + data[i[0] + count * 31:i[1]+ count * 31] + '</span>' + data[i[1]+ count * 31:]
      count += 1

    resText = Markup(data)
    print(resText)
    return render_template('index.html', input_text = inputText, res_text = resText)

if __name__ == '__main__':
    app.run()