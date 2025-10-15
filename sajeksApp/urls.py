from django.urls import path
from . import views
from . import subscription

urlpatterns = [
    path('', views.home, name ='home'),
    path('blog/', views.blog, name ='blog'),
    path('blog_detail/<int:blog_id>/', views.blog_detail, name ='blog_detail'),
    path('categories/<str:category_id>/', views.categories, name = 'categories'),
    path('tag/<str:tag_id>/', views.tag, name = 'tag'),
    path('subscribe/', subscription.subscribe_handler, name='subscribe'),
    path('videos/', views.videos, name='videos'),
    path('video_details/<int:video_id>/', views.video_details, name = 'video_details'),
    path('service/', views.service, name ='service'),
    path('about/', views.about, name ='about'),
    path('produce_list_view/', views.produce_list_view, name ='produce_list_view'),
    path('contact/', views.contact, name ='contact'),
    path('testimonial/', views.testimonial, name ='testimonial'),
    path('submit_testimonial_view/', views.submit_testimonial_view, name ='submit_testimonial_view'),
    path('contact_list/', views.contact_list, name ='contact_list'),
    path('contact_detail/<int:contact_id>/', views.contact_detail, name ='contact_detail'),
    path('mark_as_read/<int:contact_id>/', views.mark_as_read, name ='mark_as_read'),
    path('delete_contact/<int:contact_id>/', views.delete_contact, name ='delete_contact'),
    path('gallery/', views.gallery, name ='gallery'),
    path('send_newsletter_view/', views.send_newsletter_view, name ='send_newsletter_view'),
    path('unsubscribe_view/<uuid:token>/', views.unsubscribe_view, name='unsubscribe_view'),
]
