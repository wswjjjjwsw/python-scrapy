import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager as fm

# def count_element(price):


#jingdong
file_name = "Data.json"
file = open(file_name,encoding='utf-8')
list_jd = []
for line in file.readlines():
    dicc = json.loads(line)
    if dicc['price'] != "" and int(float(dicc['price'])) <10000:
        list_jd.append(int(float(dicc['price'])))

list_tb = []
file_name = "tbphone"
i = 1
while i<29:
    name = file_name+str(i)+".json"
    file = open(name, encoding='utf-8')
    for line in file.readlines():
        dicc = json.loads(line)
        if float(dicc["单价"]) != 0 and float(dicc["单价"]) < 10000:
            list_tb.append(int(float(dicc["单价"])))
    i+=1


print(min(list_tb))
print(max(list_tb))
print(min(list_jd))
print(max(list_jd))
fig,ax=plt.subplots()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

y_list = []
x_list = []
i = 0
while i <10000:
    y_list.append(0)
    x_list.append(i)
    i+=1

for each in list_tb:
    y_list[int(each)] +=1

for each in list_tb:
    if(y_list[each] == 0):
        y_list.remove(each)
        x_list.remove(each)

ax1.axis([0,10000,0,40])
ax1.scatter(x_list, y_list, s= 20)
ax1.set_title("taobao")


while i <10000:
    y_list[i] = 0
    i += 1

for each in list_jd:
    y_list[int(each)] +=1

for each in list_jd:
    if(y_list[each] == 0):
        y_list.remove(each)
        x_list.remove(each)
ax2.axis([0,10000,0,40])
ax2.scatter(x_list, y_list, s= 20)
ax2.set_title("jingdong")
plt.show()