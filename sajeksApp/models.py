import email
from django.db import models
from django.contrib.auth.models import User
import re
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid 

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
class Logo(models.Model):
    image = models.ImageField(upload_to = 'logo_img', help_text="this is the image to use on logo")
    
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
    pic = models.ImageField(upload_to='chooseus_img', null=True)
    title = models.CharField(max_length=100, null=True, help_text="The title of the why choose us pic.")
    body = CKEditor5Field(max_length = 500000, null =True, blank = True, help_text = 'Enter the video content. this field is optional')
    # list = models.CharField(max_length=500, null=True, help_text="list the important of crops")
    
    # Store the input URL
    youtube_url = models.CharField(max_length=255, blank=True, null=True)
    
    # Store the extracted, cleaned video ID (e.g., 'Nm-zMvD6MLk')
    video_id = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null = True)
    
    class Meta:
        ordering = ['-updated_on',]
        verbose_name = 'Home Video'
        verbose_name_plural = 'Home Videos'

    def __str__(self):
        return self.title or f'Home Video ({self.id})'

    # --- Methods for Automated Processing ---

    @property
    def embed_url(self):
        """
        Generates the standard YouTube embed URL using the stored video_id.
        This is the most reliable way to display the video in an iframe.
        """
        if self.video_id:
            return f'https://www.youtube.com/embed/{self.video_id}'
        
        # Fallback if no ID was found
        return self.youtube_url

    def save(self, *args, **kwargs):
        """
        Overrides save to ensure the video_id is extracted from the URL 
        before saving to the database.
        """
        if self.youtube_url:
            # This regex captures the video ID from:
            # 1. Standard watch URL (?v=ID)
            # 2. Shortened URL (youtu.be/ID)
            # 3. YouTube Shorts URL (/shorts/ID)
            # 4. Embed URL (/embed/ID)
            # Note: Bing URLs are often complex but often contain a standard YouTube ID or can be hardcoded if needed.
            # We focus on the most common YouTube formats here.
            
            # The pattern looks for the ID after 'watch?v=', 'youtu.be/', 'youtube.com/shorts/', etc.
            match = re.search(
                r'(?:youtube\.com/(?:watch\?v=|shorts/|embed/|v/)|youtu\.be/)([a-zA-Z0-9_-]+)',
                self.youtube_url
            )
            
            # Special handling for Bing URLs that might contain the YouTube ID
            if not match and 'mid=' in self.youtube_url:
                # This is a specific pattern for the Bing URL provided, extracting the GUID-like ID
                # For guaranteed YouTube playback, you'd typically ask the user to input the original YT URL.
                pass # Leave video_id as None or implement Bing-specific logic if needed.

            if match:
                self.video_id = match.group(1)
            else:
                self.video_id = None 
        else:
             self.video_id = None 

        super().save(*args, **kwargs)
    
    
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
class Subscribtion(models.Model):
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length=100)

    posted_on = models.DateTimeField(auto_now_add=True, null=True)
    
    # 🔑 NEW FIELD: Unique token for secure unsubscribing
    # default=uuid.uuid4 ensures a unique token is generated on creation
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True) 


    def __str__(self):
        return self.email
    

class About_us(models.Model):
    pic = models.ImageField(upload_to='about_img', null=True)
    title = models.CharField(max_length=100, null=True, help_text="The title of the why choose us pic.")
    body = CKEditor5Field(max_length = 500000, null =True, blank = True, help_text = 'Enter the video content. this field is optional')
    # list = models.CharField(max_length=500, null=True, help_text="list the important of crops")
    
    # Store the input URL
    youtube_url = models.CharField(max_length=255, blank=True, null=True)
    
    # Store the extracted, cleaned video ID (e.g., 'Nm-zMvD6MLk')
    video_id = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null = True)
    
    class Meta:
        ordering = ['-updated_on',]
        verbose_name = 'About'
        verbose_name_plural = 'About us'

    def __str__(self):
        return self.title or f'About us ({self.id})'

    # --- Methods for Automated Processing ---

    @property
    def embed_url(self):
        """
        Generates the standard YouTube embed URL using the stored video_id.
        This is the most reliable way to display the video in an iframe.
        """
        if self.video_id:
            return f'https://www.youtube.com/embed/{self.video_id}'
        
        # Fallback if no ID was found
        return self.youtube_url

    def save(self, *args, **kwargs):
        """
        Overrides save to ensure the video_id is extracted from the URL 
        before saving to the database.
        """
        if self.youtube_url:
            # This regex captures the video ID from:
            # 1. Standard watch URL (?v=ID)
            # 2. Shortened URL (youtu.be/ID)
            # 3. YouTube Shorts URL (/shorts/ID)
            # 4. Embed URL (/embed/ID)
            # Note: Bing URLs are often complex but often contain a standard YouTube ID or can be hardcoded if needed.
            # We focus on the most common YouTube formats here.
            
            # The pattern looks for the ID after 'watch?v=', 'youtu.be/', 'youtube.com/shorts/', etc.
            match = re.search(
                r'(?:youtube\.com/(?:watch\?v=|shorts/|embed/|v/)|youtu\.be/)([a-zA-Z0-9_-]+)',
                self.youtube_url
            )
            
            # Special handling for Bing URLs that might contain the YouTube ID
            if not match and 'mid=' in self.youtube_url:
                # This is a specific pattern for the Bing URL provided, extracting the GUID-like ID
                # For guaranteed YouTube playback, you'd typically ask the user to input the original YT URL.
                pass # Leave video_id as None or implement Bing-specific logic if needed.

            if match:
                self.video_id = match.group(1)
            else:
                self.video_id = None 
        else:
             self.video_id = None 

        super().save(*args, **kwargs)
     
   
class ProduceItem(models.Model):
    """
    Model representing a single vegetable or agricultural product available for sale.
    This replaces the general 'Service' model used previously.
    """
    # Product Identification & Content
    title = models.CharField(max_length=150, verbose_name="Product Name", help_text="e.g., Organic Cherry Tomatoes")
    slug = models.SlugField(unique=True, max_length=150, blank=True, help_text="Automatically generated from the title.")
    description = models.TextField(verbose_name="Full Description",help_text="Detailed information about the produce, growing method, and benefits.")
    
    # E-commerce Fields
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price (Kenya Shilling)",help_text="The price per unit (e.g., per Kg or per bunch).")
    unit_of_sale = models.CharField(max_length=50, default='per Kg',help_text="e.g., 'per Kg', 'per Bunch', 'per Box'")
    
    # Stock Management Field (Essential for the template logic)
    is_available = models.BooleanField(default=True, verbose_name="In Stock")
    
    # Image Field
    image = models.ImageField(upload_to='produce_images/', null=True, blank=True,verbose_name="Product Image")
    
    # Metadata
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produce Item"
        verbose_name_plural = "Produce Items"
        ordering = ['-is_available', 'title'] # Prioritize available items

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically generate a slug based on the title if it doesn't exist
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def formatted_price(self):
        """Returns the price with currency and unit."""
        return f"Ksh {self.price:.2f}/{self.unit_of_sale.replace('per ', '')}"

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject=models.CharField(max_length=50)
    message = CKEditor5Field(max_length=500)
    status = models.BooleanField(default=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['posted_on']

class adminContact(models.Model):
    location = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    call= models.CharField(max_length=50)

    def __str__(self):
        return self.location

class Testimonial(models.Model):
    full_name = models.CharField(max_length=50)
    message =models.TextField(max_length=200)
    image = models.ImageField(upload_to='testimonial_images/', null=True, blank=True,verbose_name="Product Image")

    rating = models.IntegerField(
        # default=5,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        help_text="Rating given by the client (1 to 5 stars)."
    )
    is_approved = models.BooleanField(default=False, null = True) 
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    
    # ... other fields ...
    
    def __str__(self):
        return f"{self.full_name} - {self.rating} stars"
    
    class Meta:
        ordering = ['-is_approved']
    
class Team(models.Model):
    full_name =models.CharField(max_length=50)
    role =models.CharField(max_length=50)
    image = models.ImageField(upload_to='testimonial_images/', null=True, blank=True,verbose_name="Product Image")


    def __str__(self):
        return self.full_name
    
class Team_url(models.Model):
    url = models.CharField(max_length=100, null=True, blank=True)
    team = models.ForeignKey(Team, verbose_name=("Social Handles for team members"), on_delete=models.CASCADE)
    
    def __str__(self):
        return self.url
class StanleyIntro(models.Model):
    full_name = models.CharField(max_length=50) 
    url = models.ManyToManyField(Team_url) 
    body = models.TextField(max_length=200) 
    image = models.ImageField(upload_to='stanly_image/', null=True, blank=True,verbose_name="Stanly")

class Gallary(models.Model):
    title =models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='gallary_images/', null=True, blank=True,verbose_name="Product Image")

class QuoteByCEO(models.Model):
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='CEO_images/')
    body =models.TextField(max_length=250)
    
    def __str__(self):
        return self.full_name
    