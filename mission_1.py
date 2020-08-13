import csv
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager as fm



def clean(str):
    str = str.lower()
    if str.find('荣耀') >= 0:
        str = "honor" + str
    elif str.find('华为') >= 0:
        if(str.find('huawei')< 0):
            str = "huawei" + str
    if str.find('小米') >= 0:
        if (str.find('mi')< 0):
            str = "mi" + str
    if str.find('一加') >= 0:
        if (str.find('oneplus')< 0):
            str = "oneplus" + str
    if str.find('苹果') >= 0:
        if (str.find('iphone')< 0):
            str = "iphone" + str
    str = str.replace("apple", "")
    str = str.replace("5g", "")
    str = filter(lambda ch: ch in '0123456789abcdefghijklmnopqrstuvwxyz',str)
    a = ''.join(list(str))
    return a

def clean_tb(li):
    str = ""
    flag = 0
    next_flag = 0
    for each in li:
        if each.find('产品名称') >= 0:
            flag += 1
        if (next_flag == 1):
            str = each
            next_flag = 0
        if(flag == 2):
            if(each.find('苹果') >= 0 or each.find('...') >= 0):
                next_flag=1
            else:
                str = each
            flag = -10

    str = str.lower()
    if str.find('荣耀') >= 0:
        str = "honor" + str
    elif str.find('华为') >= 0:
        if (str.find('huawei') < 0):
            str = "huawei" + str
    if str.find('小米') >= 0:
        if (str.find('mi') < 0):
            str = "mi" + str
    if str.find('一加') >= 0:
        if (str.find('oneplus') < 0):
            str = "oneplus" + str
    if str.find('苹果') >= 0:
        if (str.find('iphone') < 0):
            str = "iphone" + str
    str = str.replace("apple", "")
    str = str.replace("5g", "")
    str = str.replace(" ","")
    str = str.replace("：", "")
    str = filter(lambda chh: chh in '0123456789abcdefghijklmnopqrstuvwxyz',str)
    ss = ""
    for each in str:
        ss += each
    f = 'huawei'
    count = -1
    count = ss.find(f)
    if (count >= 0):
        if(ss[count+1:].find('f')):
            ss = ss.replace(f,"",1)
    f = 'honor'
    count = ss.find(f)
    if (count >= 0):
        if (ss[count+1:].find('f')):
            ss = ss.replace(f, "", 1)
    return ss

def purchase_number(obj):
    return obj['purchase']


#jingdong
file_name = "Data.json"
file = open(file_name,encoding='utf-8')
dic_jd = []
for line in file.readlines():
    dicc = json.loads(line)
    dicc['model'] = clean(dicc['model'])
    if dicc['model'] != "":
        dic_jd.append(dicc)



list = []
list.append({"name":"iphonexs","purchase":0})
list.append({"name":"iphonexr","purchase":0})
list.append({"name":"iphonex","purchase":0})

for each in dic_jd:
    flag = 0
    for ea in list:
        strr = each['model']
        if(strr.find(ea['name']) >= 0):
            ea['purchase'] +=each['purchase']
            flag = 1
    sstr = each['model']
    if flag == 0 and not sstr.isdigit() and not sstr.isalpha():
        new_model = {"name":each['model'],"purchase":each['purchase']}
        list.append(new_model)

list.sort(key = purchase_number,reverse = True)
print(list[:50])


#taobao
dic_tb = []
file_name = "tbphone"
i = 1
while i<29:
    name = file_name+str(i)+".json"
    file = open(name, encoding='utf-8')
    for line in file.readlines():
        dicc = json.loads(line)
        li = dicc["商品详情"].split("\n")
        dicc["商品详情"] = clean_tb(li)
        purchase_str = dicc["购买数量"]
        wan = purchase_str.find("万")
        add = purchase_str.find("+")
        purchase = 0
        if(wan >= 0):
            purchase = float(purchase_str[:wan])
            purchase = int(purchase * 10000)
        elif(add >= 0):
            for ea in range(add):
                purchase = purchase * 10 + int(purchase_str[ea])
        else:
            j = 0
            while purchase_str[j] != "人":
                purchase = purchase * 10 +int(purchase_str[j])
                j+=1
        dicc["购买数量"] = purchase
        if dicc["商品详情"] != "":
            dic_tb.append(dicc)
    i+=1

list_tb = []
for each in dic_tb:
    flag = 0
    for ea in list_tb:
        strr = each['商品详情']
        if(strr.find(ea['name']) >= 0):
            ea['purchase'] +=each['购买数量']
            flag = 1
    sstr = each['商品详情']
    if flag == 0 and not sstr.isdigit() and not sstr.isalpha():
        new_model = {"name":each['商品详情'],"purchase":each['购买数量']}
        list_tb.append(new_model)

list_tb.sort(key = purchase_number,reverse = True)
print(list_tb[:50])


fig,ax=plt.subplots()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
proptease = fm.FontProperties()
proptease.set_size('xx-small')

lix = []
liy = []
for each in list[:20]:
    lix.append(each['name'])
    liy.append(each['purchase'])
# plt.style.use('dark_background') #设置图像风格
ax1.set_title("taobao")
x = np.array(lix)
y = np.array(liy)
ax1.bar(x,y)
# plt.xticks(x, rotation=30, fontsize = 7)

for each in list_tb[:20]:
    lix.append(each['name'])
    liy.append(each['purchase'])
# plt.style.use('dark_background') #设置图像风格
ax2.set_title("jingdong")
x = np.array(lix)
y = np.array(liy)
ax2.bar(x,y)
plt.xticks(x, rotation=30, fontsize = 7)
plt.show()