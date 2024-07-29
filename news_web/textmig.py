import csv #传入新闻正文信息文件到django数据库
import ast
from datetime import datetime
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_web.settings")
django.setup()
from main.models import news,Image,Category

csv_file_path='new_output.csv'

data_to_insert = []
batch_size = 100 
category_1 = Category.objects.get(name="1月")
category_2 = Category.objects.get(name="2月")
category_3 = Category.objects.get(name="3月")
category_4 = Category.objects.get(name="4月")
category_5 = Category.objects.get(name="5月")
category_6 = Category.objects.get(name="6月")
category_7 = Category.objects.get(name="7月")
category_8 = Category.objects.get(name="8月")
category_9 = Category.objects.get(name="短讯/消息")
category_10 = Category.objects.get(name="长文/评论")
category_11 = Category.objects.get(name="数码")
category_12 = Category.objects.get(name="美股相关")
category_13 = Category.objects.get(name="科学探索")
category_14 = Category.objects.get(name="其他")

with open("new_output.csv", 'r',encoding="UTF-8") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # 跳过标题行
    for row in csvreader:
        title_1 = row[1]
        author_2 = row[2]
        publish_time_3 = row[3]
        publish_time_3="2023-"+publish_time_3
        like_num_4=int(row[4].replace(",",""))
        comment_num_5=int(row[5].replace(",",""))
        text_6=row[6]
        url_8=row[8]
        publish_time=datetime.strptime(publish_time_3,"%Y-%m-%d %H:%M")
        ap=news(title=title_1, author=author_2, pub_date=publish_time,like_num=like_num_4,comment_num=comment_num_5,text=text_6,news_url=url_8)
        ap.save()
        if publish_time.month==1:
            ap.Categories.add(category_1)
        elif publish_time.month==2:
            ap.Categories.add(category_2)
        elif publish_time.month==3:
            ap.Categories.add(category_3)
        elif publish_time.month==4:
            ap.Categories.add(category_4)
        elif publish_time.month==5:
            ap.Categories.add(category_5)
        elif publish_time.month==6:
            ap.Categories.add(category_6)
        elif publish_time.month==7:
            ap.Categories.add(category_7)
        elif publish_time.month==8:
            ap.Categories.add(category_8)
        if len(text_6)<=500:
            ap.Categories.add(category_9)
        else:
            ap.Categories.add(category_10)
        if url_8[28:33]=="stock":
            ap.Categories.add(category_12)
        elif url_8[33:37]=="digi":
            ap.Categories.add(category_11)
        elif url_8[33:42]=="discovery":
            ap.Categories.add(category_13)
        else:
            ap.Categories.add(category_14)
        

# 插入剩余数据
if data_to_insert:
    news.objects.bulk_create(data_to_insert)
print("数据导入完成")
