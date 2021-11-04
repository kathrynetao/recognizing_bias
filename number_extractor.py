import re
def number_extract(article):
    reg_list = ['\d+\.?\d*(?:\s*%| per\s*cent)','(?:\$\s*|\￥\s*)*\d+\.+\d+','\d+[,]+\d+','["]+.*["]+']
    found_reg_list = []
    for reg in reg_list:
        answer = re.findall(reg,article)
        found_reg_list.append(answer)
    return found_reg_list


s  = "3.7% $ 10.00,￥10.11, 7.777 %, 10%, 75.777 percent, 82.77% 82.77 per cent 1,000, \"100 billion\"."
a = number_extract(s)
print(a)

