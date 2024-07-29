import matplotlib.pyplot as plt
import os
import django
import jieba
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_web.settings")
django.setup()
from main.models import news,Image,Category,Comment,InvertedIndex
from django.shortcuts import render,get_object_or_404,redirect
import main.views
from django.db.models import Q
categories=Category.objects.all()
kinds={1: 1032, 2: 627, 3: 403, 4: 663, 5: 858, 6: 957, 7: 837, 8: 776, 9: 2076, 10: 4077, 11: 442, 12: 276, 13: 307, 14: 5128}
words=['AI','三体','iphone','特斯拉']
for query in words:
    news_num=dict()
    for i in range(1,9):
        tp=get_object_or_404(Category,pk=i)
        news_tp=tp.news_set.all()
        news_list = news_tp.filter(Q(title__icontains=query) | Q(text__icontains=query))
        news_num[i]=len(news_list)
    print(news_num)
    scale=dict()
    for i in range(1,9):
        scale[i]=round(news_num[i]/kinds[i],3)
    x=list()
    y=list()
    for i in range(1,9):
        x.append(i)
        y.append(scale[i])
    plt.plot(x,y)
plt.rcParams['font.sans-serif']=['SimHei']#解决中文乱码
plt.rcParams['axes.unicode_minus']=False
plt.legend(words, loc='upper left')
plt.show()
