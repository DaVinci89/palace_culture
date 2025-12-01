from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('<slug:slug>/add-comment/', views.AddCommentView.as_view(), name='add_comment'),
    #path('gallery/', views.GalleryListView.as_view(), name='gallery_list'),
]