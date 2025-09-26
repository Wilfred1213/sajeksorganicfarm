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
@admin.register(Homevideo)
class HomeVideosAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_id', 'youtube_url')
    # Make the other fields read-only since they are populated automatically
    readonly_fields = ('video_id', 'title', 'pic', 'body')
    fields = ('youtube_url', 'title', 'pic', 'body')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'content', 'blog')
    # Make the other fields read-only since they are populated automatically
    readonly_fields = ('img', 'email', 'full_name', 'content')
    # fields = ('youtube_url', 'title', 'pic', 'body')
