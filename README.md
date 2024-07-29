# 爬虫与信息系统研究报告
## *1.爬虫*
爬虫部分使用selenium结合webdriver模拟浏览器操作进行新闻爬取（爬取对象来源为新浪微博），首先访问不同日期的滚动新闻页面爬取各项新闻的正文页url，再依次访问正文页url进行新闻详细信息的爬取。爬取信息后保存到本地csv文件（图片先保存相应url，再根据url下载图片到本地）（对应代码为crawl_for_news文件夹下的crawl.py和group_crawl.ipynb）。 总新闻数量6K+，图片数量18K+。
   
在爬取新闻正文时先使用了list数据形式进行存储，再将其转换为str类型同时添加换行符。（对应代码为crawl_for_news文件夹下的text_reload.py）  
## *2.信息写入django数据库*
我在django的models.py中定义了news、Category、Comment和Image四个模型，其中Category为news的外键，news为Comment和Image的外键。在写入数据时，先将新闻正文页除图片外的信息写入news、根据新闻类型（时间、篇幅、主题）添加对应的category作为外键（对应代码news_we\/textmig.py)，再将图片url写入Image、同时添加对应的所属新闻news作为外键（对应news_web\imgmig.py),再访问图片url爬取图片到本地（news_web\download.py)。  
models.py中还定义了InvertedIndex模型，用于后续构建倒排索引使用。 
## *3.web网页设计*
web设计部分我在news_web/main/templates/main文件夹下建立了main.html、news_list.html、news_detail.html、search.html、search_results.html、category.html、category_detail.html七个html文件，分别对应主页、新闻列表页、新闻正文页、搜索页、搜索结果页、分类页、分类结果页的实现；对于每个html文件，news_web/main文件夹下的views.py中定义了相应的同名视图函数将有关参数传递给html文件。除此之外，views.py中还建立了delete_comment()函数用于删除评论并重定向到新闻正文页。

各部分网页的主要功能如分页、搜索、分类、评论、随机新闻展示等均按实验内容要求完成，在此不再赘述。此外，还在所有网页顶端添加了导航栏用于各基本网页间的跳转。
![主页图](.\news_web\主页.png "main")
在新闻列表页、搜索结果页等部分还实现了显示“封面图”的功能（有图的新闻显示第一张图，无图新闻则显示默认封面图片,下图第一条新闻图片为默认封面图）。
![列表页图](.\news_web\列表页.png "list")
美化方面，主要通过修改html文件内style标签的各项参数完成，少量使用的图标来自[此链接](https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css).  

搜索性能方面，news_web/invertindex.py结合jieba的中文分词功能建立了倒排索引数据库，储存到InvertIndex模型数据库中。InvertIndex模型储存的信息包括词语名(word)、含有该词语的新闻id(news_id)、词频(frequency)。在搜索时，将首先将输入各部分使用jieba进行中文分词，再将各分词在InvertIndex数据库中进行查找，找到新闻id属于所有分词InvertIndex.news_id的新闻进行呈现，从而加速搜索速度。同时实现了在完全匹配无结果时，能够匹配到包含所有分词的新闻（添加倒排索引的索引数据对应代码为news_web\invertindex.py)。  
考虑到部分搜索词可能不在数据库中，当上一步得到的新闻数量为0时，会再进行一次直接精确查找，尽可能避免无结果的情况出现（如搜索Huawei和uawei时，均能找到所有包含Huawei的文章，当然前者通过倒排索引实现速度更快）。  
总共建立的InvertIndex词语索引数量138K+。
## *4.数据分析与可视化*
详见data_analysis\数据分析报告.md
## *5.感想*
完成这次大作业的过程实属坎坷。在爬虫部分就踩了不少的坑：先是在试图使用request爬取时因为目标网页（腾讯新闻）为动态流形式而失败，在学习了selenium后试着爬取腾讯新闻又发现可爬取的新闻总数有限，不得不全部推倒重来；转而爬取新浪微博时又因为新浪的新闻html格式种类过多而增加了代码量；模拟浏览器的运行速度也过慢，在教室一下午也只爬取了不足两千条。完成任务所用的学习、测试的沉没成本实在太多，但确实在这个过程中学到了更多关于爬虫的知识，这也让我在碰壁后能及时调整完善代码。  
在web设计过程中，我结合chatGPT探索了很多html可以实现的格式上的美化，包括为文本框添加阴影、渐变色等等，见证了html中蕴含的无限可能；搜索性能方面优化的学习也让我积累了许多经验。  
已经记不清各个部分到底耗时分别有多少，只知道过去一个星期每天都能学习测试到自习室关门hhhh。正如老师上课所说“在这个过程中学到知识才最为重要”，实验的过程虽然艰辛，但也确有学习知识的喜悦。