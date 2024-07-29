from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from .models import news,Image,Category,Comment,InvertedIndex
from django.db.models import Q
from time import time as tm
import jieba
# Create your views here.
def main(request):
    random_news=news.objects.order_by('?')[:20]
    template = loader.get_template('main/main.html')
    category_list=Category.objects.all()
    time=[]
    size=[]
    topic=[]
    for i in category_list:
        if i.name[1]=='月':
            time.append(i)
        elif i.name=='短讯/消息' or i.name=='长文/评论':
            size.append(i)
        else:
            topic.append(i)
    context={
        'time_categories':time,
        'size_categories':size,
        'topic_categories':topic,
        'categories':category_list,
        'random_news': random_news,
    }
    return HttpResponse(template.render(context, request))
def news_detail(request, pk):
    news_item = get_object_or_404(news, pk=pk)
    news_text=news_item.text.split("\n")
    images=news_item.image_set.all()
    comments = Comment.objects.filter(news_origin=news_item).order_by('-created_at')

    if request.method == "POST":
        comment_text = request.POST.get("comment_text")
        if comment_text:
            Comment.objects.create(text=comment_text, news_origin=news_item)
            return redirect('news_detail', pk=pk)  # 重定向到新闻正文页

    comments = Comment.objects.filter(news_origin=news_item).order_by('-created_at')
    return render(request, 'main/news_detail.html', {'news_item': news_item, 'news_text': news_text, 'images': images, 'comments': comments})
def news_list(request):
    news_list=news.objects.all()
    per_page = 20
    paginator = Paginator(news_list, per_page)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    else:
        page_number = int(page_number)
    nearby_pages = range(max(page_number - 2, 1), min(page_number + 3, paginator.num_pages + 1))
    news_page = paginator.get_page(page_number)
    return render(request, 'main/news_list.html',{'news_list':news_page,'nearby_pages':nearby_pages})
def category_detail(request,pk):
    kind=get_object_or_404(Category,pk=pk)
    news_list=kind.news_set.all()
    per_page = 20
    paginator = Paginator(news_list, per_page)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    else:
        page_number = int(page_number)
    nearby_pages = range(max(page_number - 2, 1), min(page_number + 3, paginator.num_pages + 1))
    news_page = paginator.get_page(page_number)
    return render(request,'main/category_detail.html',{'news_list':news_page,'kind':kind,'nearby_pages':nearby_pages})
def category(request):
    category_list=Category.objects.all()
    time=[]
    size=[]
    topic=[]
    for i in category_list:
        if i.name[1]=='月':
            time.append(i)
        elif i.name=='短讯/消息' or i.name=='长文/评论':
            size.append(i)
        else:
            topic.append(i)
    context={
        'time_categories':time,
        'size_categories':size,
        'topic_categories':topic,
    }
    return render(request,'main/category.html',context)
def delete_comment(request,pk,comment_id):
    comment=get_object_or_404(Comment,pk=comment_id)
    comment.delete()
    return redirect('news_detail',pk=pk)
def search(request):
    category_list=Category.objects.all()
    time=[]
    size=[]
    topic=[]
    for i in category_list:
        if i.name[1]=='月':
            time.append(i)
        elif i.name=='短讯/消息' or i.name=='长文/评论':
            size.append(i)
        else:
            topic.append(i)
    context={
        'time_categories':time,
        'size_categories':size,
        'topic_categories':topic,
        'categories':category_list,
    }
    return render(request,'main/search.html',context)
def search_results(request):
    start_time = tm()
    query = request.GET.get('q', '')
    query_words=jieba.lcut_for_search(query)
    matching_doc_ids = set()
    word_index=0
    for word in query_words:
        try:
            index_entry = InvertedIndex.objects.get(word=word)
            doc_ids = map(int, index_entry.news_ids.split(','))
            if word_index==0:
                matching_doc_ids.update(doc_ids)
                word_index+=1
            else:
                doc_ids=set(doc_ids)
                matching_doc_ids=matching_doc_ids-(matching_doc_ids-doc_ids)
        except InvertedIndex.DoesNotExist:
            matching_doc_ids = set()
            break
    news_list = news.objects.filter(id__in=matching_doc_ids).distinct()
    if len(news_list)==0:#倒排索引失效时，转用精确检索一遍，避免搜索无结果出现
        news_list = news.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
    selected_categories = request.GET.getlist('categories')
    sort_option = request.GET.get('sort', 'time')
    if selected_categories:
        news_list = news_list.filter(Categories__in=selected_categories)
    if sort_option == 'hot':
        news_list = news_list.order_by('-like_num')
    else:
        news_list = news_list.order_by('-pub_date')
    per_page = 20
    paginator = Paginator(news_list, per_page)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    else:
        page_number = int(page_number)
    nearby_pages = range(max(page_number - 2, 1), min(page_number + 3, paginator.num_pages + 1))
    news_page = paginator.get_page(page_number)
    end_time = tm()
    time=end_time-start_time
    k=len(news_list)
    context = {
        'query': query,
        'news_list': news_page,
        'categories': selected_categories,
        'all_news':k,
        'nearby_pages':nearby_pages,
        'time':round(time,3),
        'sort_type':sort_option,
    }
    return render(request, 'main/search_results.html', context)