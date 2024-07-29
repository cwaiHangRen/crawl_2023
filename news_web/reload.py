import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_web.settings")
django.setup()
from main.models import news,Image,Category,Comment
import requests

download_folder = ''
image_list=Image.objects.all()
num=0
for one in image_list:
    base_url=one.url
    file_name = os.path.join(download_folder, os.path.basename(base_url))
    one.image_file = file_name
    one.save()
