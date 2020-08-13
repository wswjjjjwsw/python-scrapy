import csv
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager as fm


def makelist(y1, y2):
    i = j = k = 0
    x1 = []
    x2 = []
    while (i < len(y1) and j < len(y2)):
        if (y1[i] < y2[j]):
            j += 1
            x2.append(k)
        else:
            i += 1
            x1.append(k)
        k += 1

    while i < len(y1):
        x1.append(k)
        k += 1
        i += 1

    while j < len(y2):
        x2.append(k)
        k += 1
        j += 1

    return x1, x2


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


for each in dic_jd:
    flag = 0
    strr = each['model']
    for ea in list:
        if(strr.find(ea) >= 0):
            each['model'] = ea
            flag = 1
    if flag == 0 and not strr.isdigit() and not strr.isalpha():
        list.append(strr)


print(dic_jd)


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
    strr = each['商品详情']
    for ea in list_tb:

        if(strr.find(ea) >= 0):
            each['商品详情'] = ea
            flag = 1
    if flag == 0 and not strr.isdigit() and not strr.isalpha():
        list.append(strr)

print(dic_tb)


jd_hm30 = []
jd_ip11 = []
jd_rmn8 = []
jd_h20 = []
jd_h9x = []

tb_hm30 = []
tb_ip11 = []
tb_rmn8 = []
tb_h20 = []
tb_h9x = []

for each in dic_tb:
    if(each['商品详情'] ==  "huaweimate30"):
        tb_hm30.append(int(float(each["单价"])))
    if (each['商品详情'] == "iphone11"):
        tb_ip11.append(int(float(each["单价"])))
    if (each['商品详情'] == "redminote8"):
        tb_rmn8.append(int(float(each["单价"])))
    if (each['商品详情'] == "honor20"):
        tb_h20.append(int(float(each["单价"])))
    if (each['商品详情'] == "honor9x"):
        tb_h9x.append(int(float(each["单价"])))




for each in dic_jd:
    if(each['model'] == "huaweimate30"):
        jd_hm30.append(int(float(each['price'])))
    if (each['model'] == "iphone11"):
        jd_ip11.append(int(float(each['price'])))
    if (each['model'] == "redminote8"):
        jd_rmn8.append(int(float(each['price'])))
    if (each['model'] == "honor20"):
        jd_h20.append(int(float(each['price'])))
    if (each['model'] == "honor9x"):
        jd_h9x.append(int(float(each['price'])))

tb_hm30.sort(reverse=True)
tb_ip11.sort(reverse=True)
tb_rmn8.sort(reverse=True)
tb_h20.sort(reverse=True)
tb_h9x.sort(reverse=True)

jd_hm30.sort(reverse=True)
jd_ip11.sort(reverse=True)
jd_rmn8.sort(reverse=True)
jd_h20.sort(reverse=True)
jd_h9x.sort(reverse=True)

fig,ax=plt.subplots()
ax1 = fig.add_subplot(231)
ax2 = fig.add_subplot(232)
ax3 = fig.add_subplot(233)
ax4 = fig.add_subplot(234)
ax5 = fig.add_subplot(235)

x1,x2 = makelist(tb_hm30,jd_hm30)
ax1.bar(x1, tb_hm30, align =  'center')
ax1.bar(x2, jd_hm30, align =  'center')
ax1.set_title("Huawei Mate 30")

x1,x2 = makelist(tb_ip11,jd_ip11)
ax2.bar(x1, tb_ip11, align =  'center')
ax2.bar(x2, jd_ip11, align =  'center')
ax2.set_title("iPhone 11")

x1,x2 = makelist(tb_rmn8,jd_rmn8)
ax3.bar(x1, tb_rmn8, align =  'center')
ax3.bar(x2, jd_rmn8, align =  'center')
ax3.set_title("Redmi note 8")

x1,x2 = makelist(tb_h20,jd_h20)
ax4.bar(x1, tb_h20, align =  'center')
ax4.bar(x2, jd_h20, align =  'center')
ax4.set_title("Honor 20")

x1,x2 = makelist(tb_h9x,jd_h9x)
ax5.bar(x1, tb_h9x, align =  'center')
ax5.bar(x2, jd_h9x, align =  'center')
ax5.set_title("Honor 9x")

plt.show()