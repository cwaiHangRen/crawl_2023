import csv   #将正文内容转换为str（带换行符）存储
import ast
data=[]
with open('data.csv', 'r',encoding="UTF-8") as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        data.append(row)
for i in data:
    if(i==data[0]):
        continue
    a=""
    b=ast.literal_eval(i[5])
    b=list(b)
    for j in b:
        a+=j
        a+="\n"
    i[5]=a
with open("output.csv", 'w+', newline='',encoding="UTF-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in data:
        csvwriter.writerow(row)