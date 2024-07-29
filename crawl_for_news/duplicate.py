import shutil   #对新闻进行去重，避免分组爬虫时出现bug
import pandas as pd
 
 
frame=pd.read_csv('output.csv',engine='python')
data = frame.drop_duplicates(keep='first', inplace=False)
data.to_csv('new_output.csv', encoding='utf8')