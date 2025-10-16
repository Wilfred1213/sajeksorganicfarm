from django.contrib import admin
from sajeksApp.models import *

# Register your models here.
admin.site.register(Carousel)
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Services)
admin.site.register(Whychooseus)
admin.site.register(Whychooseuspix)
admin.site.register(Tags)
admin.site.register(Subscribtion)
admin.site.register(Team)
admin.site.register(Gallary)
admin.site.register(StanleyIntro)

@admin.register(Homevideo)
class HomeVideosAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_id', 'youtube_url')
    # Make the other fields read-only since they are populated automatically
    # readonly_fields = ('video_id', 'title', 'pic', 'body')
    fields = ('youtube_url', 'title', 'pic', 'body')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'content', 'blog')
    # Make the other fields read-only since they are populated automatically
    readonly_fields = ('img', 'email', 'full_name', 'content')
    # fields = ('youtube_url', 'title', 'pic', 'body')

@admin.register(About_us)
class HomeVideosAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_id', 'youtube_url')
    # Make the other fields read-only since they are populated automatically
    # readonly_fields = ('video_id', 'title', 'pic', 'body')
    fields = ('youtube_url', 'title', 'pic', 'body')
    
@admin.register(ProduceItem)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'is_available')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'email', 'subject', 'status')

@admin.register(adminContact)
class adminContact(admin.ModelAdmin):
    list_display = ('location', 'email', 'call')

@admin.register(Testimonial)
class TestimonialContact(admin.ModelAdmin):
    list_display = ('full_name', 'message', 'image')

@admin.register(Team_url)
class TeamUrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'team')