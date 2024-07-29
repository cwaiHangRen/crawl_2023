import csv   #传入图片信息文件到django数据库
import ast
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_web.settings")
django.setup()
from main.models import news,Image



img_to_insert=[]

with open("new_output.csv", 'r',encoding="UTF-8") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # 跳过标题行
    for row in csvreader:
        imgs=ast.literal_eval(row[7])
        imgs=list(imgs)
        url_8=row[8]
        try:
            my_news=news.objects.get(news_url=url_8)
        except:
            continue
        for i in imgs:
            if i!=None:
                imgs=Image(news_origin=my_news,url=i)
                imgs.save()

# 插入剩余数据
print("数据导入完成")
