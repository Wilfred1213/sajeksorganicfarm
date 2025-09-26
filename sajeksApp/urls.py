from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('blog/', views.blog, name ='blog'),
    path('blog_detail/<int:blog_id>/', views.blog_detail, name ='blog_detail'),
    path('categories/<str:category_id>/', views.categories, name = 'categories'),
    path('tag/<str:tag_id>/', views.tag, name = 'tag'),

]
