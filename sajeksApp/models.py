import email
from django.db import models
from django.contrib.auth.models import User
import re
from django_ckeditor_5.fields import CKEditor5Field

class Carousel(models.Model):
    title= models.CharField(max_length=100, null= True, help_text="Heading of the carousel.")
    discription = models.CharField(max_length=500, null=True, help_text="content of the carousel")
    pic = models.ImageField(upload_to = 'carousel_img', null=True)
    
    def __str__(self):
        return self.title
class Services(models.Model):
    title= models.CharField(max_length=100, null= True, help_text="Heading of the service.")
    discription = models.CharField(max_length=500, null=True, help_text="content of the discription")
    pic = models.ImageField(upload_to = 'service_img', null=True, blank=True, help_text="this is the first picture for about us")
    pic_service = models.ImageField(upload_to = 'service_img', null=True, help_text="this is the real life picture domestration")
    
    def __str__(self):
        return self.title
class Whychooseus(models.Model):
    title =models.CharField(max_length=100, null= True, help_text="The title of the Why choose us.")
    icon=  models.CharField(max_length=500, null=True, help_text="the icon to be display in safe pipe")
    body=  models.CharField(max_length=500, null=True, help_text="discription")
    
    def __str__(self):
        return self.title
    
class Whychooseuspix(models.Model):
    pic = models.ImageField(upload_to = 'chooseus_img', null=True)
    title =models.CharField(max_length=100, null= True, help_text="The title of the Why choose us pic.")
    body=  models.CharField(max_length=500, null=True, help_text="discription")
    
class Homevideo(models.Model):
    pic = models.ImageField(upload_to = 'chooseus_img', null=True)
    title =models.CharField(max_length=100, null= True, help_text="The title of the Why choose us pic.")
    body=  models.CharField(max_length=500, null=True, help_text="discription")
    list=  models.CharField(max_length=500, null=True, help_text="list the important of crops")
    
    youtube_url = models.CharField(max_length=255, blank=True, null=True)
    
    video_id = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Regular expression to extract the video ID from any YouTube URL format
        if self.youtube_url:
            match = re.search(r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)', self.youtube_url)
            if match:
                self.video_id = match.group(1)
            else:
                self.video_id = None  # Clear the ID if the URL is not valid
        
        super().save(*args, **kwargs)

        def __str__(self):
            return self.title or 'Home Video'
    
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, help_text="A URL-friendly short label.")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="A URL-friendly short label.")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    img = models.ImageField(upload_to = 'blog_img', null=True, help_text='Upload the first image for this post')
    content = CKEditor5Field('Text', config_name='extends')
    blockquote = models.CharField(max_length=255, null=True, blank=True, help_text='Optional Quote. If you have a special short quote to support this post')
    img2 = models.ImageField(upload_to = 'blog_img', null=True, blank=True, help_text='Upload the optional second image for this post')
    content2 = CKEditor5Field(max_length = 500000, null =True, blank = True, help_text = 'Option. If you want to add second post to back up the second image you uploaded')
    
    categories = models.ManyToManyField(Category, related_name='posts')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name='tags', null=True, blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class Comment(models.Model):
    full_name=models.CharField(max_length=1000)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = CKEditor5Field(max_length = 1000, null=True, blank =True)
    # reply field
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    email = models.EmailField(max_length=100, null=True, blank=True)
    website = models.URLField(max_length=100, null =True, blank=True)
    img = models.ImageField(upload_to = 'blog_img', null=True, blank=True, help_text='Upload the optional image for this post')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)



class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='video_posts')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class HomePage(models.Model):
    headline = models.CharField(max_length=255)
    hero_image = models.ImageField(upload_to='home_page_images/', help_text="Image for the hero section of the homepage.")
    about_us_text = models.TextField()
    mission_statement = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Homepage Content"
    
# models.py for a 'farm' app


class Livestock(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField(blank=True)
    # Add other unique fields like 'photo' or 'date_of_birth'
    
    def __str__(self):
        return f"{self.name} ({self.breed})"

class Greenhouse(models.Model):
    name = models.CharField(max_length=100)
    size_sq_ft = models.IntegerField()
    description = models.TextField(blank=True)
    current_crops = models.CharField(max_length=255)
    # Add other unique fields like 'temperature_sensor_data'
    
    def __str__(self):
        return self.name

class OpenField(models.Model):
    name = models.CharField(max_length=100)
    size_acres = models.DecimalField(max_digits=5, decimal_places=2)
    current_crops = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # Add other unique fields like 'last_fertilization_date'
    
    def __str__(self):
        return self.name