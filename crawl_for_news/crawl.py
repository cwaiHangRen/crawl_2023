from selenium import webdriver   #基础爬虫文件，考虑到数据量较大进行了分组爬虫后合并
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
import csv
days={"01":31,"02":28,"03":31,"04":30,"05":31,"06":30,"07":31,"08":30}
news_item=dict(title="",author="",publish_time="",like_num=0,comment_num=0,news_text=[],news_img=[],news_url="")
news_num=0

csv_data = open('news_data0.csv', 'a+', encoding="utf-8")#打开csv文件
option = webdriver.EdgeOptions()
option.add_argument('headless')
for month in list(days):
    for day in range(1,days[month]+1):
        if month=="06" and day<2:
            continue
        elif month=="08" and day<16:
            continue
        if day<10:
            date_2023="2023-"+month+"-0"+str(day)
        else:
            date_2023="2023-"+month+"-"+str(day)
        base_url=f"https://news.sina.com.cn/roll/#pageid=153&lid=2515&etime=1669392000&stime=1669478400&ctime=1669478400&date={date_2023}&k=&num=50&page=1"
        print(base_url)
        web=webdriver.Edge(options=option)
        web.get(base_url)
        news=web.find_elements(By.XPATH,"//li")
        time.sleep(0.5)
        if len(news)==0:
            break
        for j in range(len(news)):
            news_item["news_url"]=news[j].find_elements(By.XPATH,"//span[2]/a")[j].get_attribute("href")
            news_item["title"]=news[j].find_elements(By.XPATH,"//span[2]/a")[j].text
            news_item["publish_time"]=news[j].find_elements(By.XPATH,"//span[3]")[j].text
            try:
                news_web=webdriver.Edge(options=option)
                news_web.get(news_item["news_url"])
            except:
                continue
            print(news_item["news_url"])
            time.sleep(0.5)
            try:
                if news_item["news_url"][33:36]=="csj":
                    news_item["author"]=news_web.find_element(By.CLASS_NAME,"author").text
                    news_item["news_text"]=[i.text for i in news_web.find_elements(By.XPATH,"/html/body/div[4]/div[5]/div[1]/div[1]/div[1]/div[3]/p")]
                    news_item["news_img"]=[i.get_attribute("src") for i in news_web.find_elements(By.XPATH,'//div[@class="img_wrapper"]/img')]
                    news_item["like_num"]=re.findall(r'<em><a.*?>(.*?)</a>',news_web.find_element(By.XPATH,'//*').get_attribute("outerHTML"))[1]
                    news_item["comment_num"]=re.findall(r'<em><a.*?>(.*?)</a>',news_web.find_element(By.XPATH,'//*').get_attribute("outerHTML"))[0]
                elif news_item["news_url"][33:38]=="apple":
                    continue
                elif news_item["news_url"][33:41]=="internet":
                    news_item["author"]=re.findall(r'ent-source">(.*?)</span>',news_web.find_element(By.XPATH,'//*').get_attribute("outerHTML"))[0]
                    news_item["author"]=re.findall(r'class="source">(.*?)</span>',news_web.find_element(By.XPATH,'//*').get_attribute("outerHTML"))[0]
                    news_item["news_text"]=[i.text for i in news_web.find_elements(By.XPATH,"/html/body/div[3]/div[4]/div[1]/div[2]/p")]
                    news_item["news_img"]=[i.get_attribute("src") for i in news_web.find_elements(By.XPATH,'//div[@class="img_wrapper"]/img')]
                    news_item["like_num"]=re.findall(r'<em><a.*?>(.*?)</a>',news_web.find_element(By.XPATH,'//*').get_attribute("outerHTML"))[1]
                    news_item["comment_num"]=re.findall(r'<em><a.*?>(.*?)</a>',news_web.find_element(By.XPATH,'//*').get_attribute("outerHTML"))[0]
                else:
                    news_item["author"]=news_web.find_element(By.CLASS_NAME,"source").text
                    news_item["news_text"]=[i.text for i in news_web.find_elements(By.XPATH,"/html/body/div[3]/div[4]/div[1]/div[2]/p")]
                    if len(news_item["news_text"])==0:
                        news_item["news_text"]=[i.text for i in news_web.find_elements(By.XPATH,"/html/body/div[2]/div[4]/div[1]/div[2]/p")]
                    if len(news_item['news_text'])==0:
                        continue
                    news_item["news_img"]=[i.get_attribute("src") for i in news_web.find_elements(By.XPATH,'//div[@class="img_wrapper"]/img')]
                    news_item["like_num"]=re.findall(r'<em><a.*?>(.*?)</a>',news_web.find_element(By.XPATH,'//*').get_attribute("outerHTML"))[1]
                    news_item["comment_num"]=re.findall(r'<em><a.*?>(.*?)</a>',news_web.find_element(By.XPATH,'//*').get_attribute("outerHTML"))[0]
                if len(news_item['news_text'])==0:
                        continue
                news_num+=1
                news_web.close()
                print(news_num)
                csv.writer(csv_data).writerow([news_item["title"],news_item["author"],news_item["publish_time"],news_item["like_num"],news_item["comment_num"],news_item["news_text"],news_item["news_img"],news_item["news_url"]])
            except:
                news_web.close()
                continue
        web.close()
csv_data.close()