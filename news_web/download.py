import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_web.settings")
django.setup()
from main.models import news,Image,Category,Comment
import requests

download_folder = 'main/images'
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
image_list=Image.objects.all()
num=0
for one in image_list:
    base_url=one.url
    response=requests.get(base_url)
    if response.status_code == 200:
            # 提取文件名
        file_name = os.path.join(download_folder, os.path.basename(base_url))
            # 保存图片到本地
        with open(file_name, 'wb') as f:
                f.write(response.content)
        num+=1
        print(num)
        one.image_file = os.path.join(download_folder, )
        one.save()
    else:
        print(f"无法下载: {base_url}")
