from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('news_list/',views.news_list,name='news_list'),
    path('news_detail/<int:pk>/',views.news_detail,name='news_detail'),
    path('category/<int:pk>/',views.category_detail,name='category_detail'),
    path('category/',views.category,name='category'),
    path('search/',views.search,name='search'),
    path('search_results/',views.search_results,name='search_results'),
    path('news_detail/<int:pk>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]