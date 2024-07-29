import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_web.settings")
django.setup()
from main.models import news,Image,Category,Comment,InvertedIndex
from collections import Counter
import re
import jieba

if __name__=="__main__":
    all_news = news.objects.all()
    inverted_index = {}
    junk={"，","。","；","：","“","”","\n",":",",",".","《","》","【","】","（","）","、","(",")"}
    for news in all_news:
        # 合并标题和正文内容，将它们分成单词
        text = f"{news.title} {news.text}"
        words = jieba.lcut_for_search(text)

        # 统计单词频率
        word_freq = Counter(words)
        # 更新倒排索引
        for word, freq in word_freq.items():
            if word in junk:
                continue
            elif word in inverted_index:
                inverted_index[word]['news_ids'].append(news.id)
                inverted_index[word]['frequency'] += freq
            else:
                inverted_index[word] = {'news_ids': [news.id], 'frequency': freq}

    # 保存倒排索引到数据库
    for word, data in inverted_index.items():
        InvertedIndex.objects.create(
            word=word,
            news_ids=','.join(map(str, data['news_ids'])),
            frequency=data['frequency']
        )