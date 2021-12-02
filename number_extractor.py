import re
from nltk.tokenize import sent_tokenize, word_tokenize

def tokenize(str):
    token_words = word_tokenize(str)
    return token_words

def number_extract(article):
    # reg_list = ['\d+\.?\d*(?:\s*%| per\s*cent)','(?:\$\s*|\￥\s*)*\d+\.+\d+','\d+[,]+\d+']
    reg_list = ['\d+\.?\d*(?: \s*percent | \s*per\s*cent)+','\d+[,]+\d+','(?:\$\s*|\￥\s*)+\d+\.+\d+']
    found_reg_list = []
    iter_list = []
    #to save index [start:end] of a number
    index_list = []
    for reg in reg_list:
        answer = re.findall(reg,article)
        iter_list.append(re.finditer(reg, article))
        found_reg_list.append(answer)

    #we only want the number appear once
    start_set = set([])
    for i in range(len(iter_list)):
        for match in iter_list[i]:
            s = match.start()
            if s in start_set:
                continue
            else:
                start_set.add(s)
                e = match.end()
                index_list.append((s,e))
                # print('String match "%s" at %d:%d' % (article[s:e], s, e))
    index_list.sort()
    return found_reg_list,index_list
def get_number(article):
    word_tokenize = tokenize(article)
    numbers_stack = []
    results = []
    for word in word_tokenize:
        numbers_stack.append(word)
        if word == '%':
            numbers = []
            for i in range(3):
                numbers.append(numbers_stack[-1])
                numbers_stack.pop()
            results.append(numbers)
    return results

def highlight_number(html,article):
    numbers_token = get_number(article)
    for number in numbers_token:
        str = number[2] + " " + number[1] + number[0]
        html = html.replace(str,number[2] + " "'<span class = "numbers">'+number[1]+number[0]+'</span>')
    found_reg_list,index_list = number_extract(article)
    for word_lst in found_reg_list:
        for word in word_lst:
            html = html.replace(word,'<span class = "numbers">'+word+'</span>')
    return html

s  = "2,000 3.7% $ 10.00,￥10.11, 7.777, 10%, 75.777 percent, 82.77% 82.77 per cent 1,000, \"100 billion\"."

found_reg_list , index_list = number_extract(s)
