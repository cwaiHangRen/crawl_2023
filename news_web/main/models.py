from django.db import models
from django.utils import timezone
from collections import Counter
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=20)
class news(models.Model):
    like_num=models.IntegerField(default=0)
    comment_num=models.IntegerField(default=0)
    comment_count=models.IntegerField(default=0)
    title=models.CharField(max_length=200)
    text=models.CharField(max_length=100000)
    news_url=models.URLField()
    pub_date = models.DateTimeField()
    author=models.CharField(max_length=30)
    Categories=models.ManyToManyField(Category)
    def __str__(self):
        return self.news_url
class Image(models.Model):
    url = models.URLField()
    news_origin=models.ForeignKey(news,on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/',default=r"default.jpg")
    def __str__(self):
        return self.url
class Comment(models.Model):
    text=models.CharField(max_length=200)
    user_name=models.CharField(default="user",max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    news_origin=models.ForeignKey(news,on_delete=models.CASCADE)
class InvertedIndex(models.Model):
    word = models.CharField(max_length=50)
    news_ids = models.TextField()  # 包含该单词的新闻ID列表，以逗号分隔
    frequency = models.IntegerField()  # 单词在文档中的出现频率
    def __str__(self):
        return self.word


