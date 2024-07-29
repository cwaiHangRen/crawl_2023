from django.contrib import admin
from .models import news,Image,Category,Comment,InvertedIndex
# Register your models here.
admin.site.register(news)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(InvertedIndex)