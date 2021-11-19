import re
def number_extract(article):
    # reg_list = ['\d+\.?\d*(?:\s*%| per\s*cent)','(?:\$\s*|\￥\s*)*\d+\.+\d+','\d+[,]+\d+']
    reg_list = ['\d+\.?\d*(?:\s*%| per\s*cent)','\d+[,]+\d+','(?:\$\s*|\￥\s*)*\d+\.+\d+','(?:\$\s*|\￥\s*)+\d+\.?\d+']
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


s  = "2,000 3.7% $ 10.00,￥10.11, 7.777, 10%, 75.777 percent, 82.77% 82.77 per cent 1,000, \"100 billion\"."
found_reg_list , index_list = number_extract(s)
print(found_reg_list)

