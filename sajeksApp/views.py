from itertools import count
from typing import Counter
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from sajeksApp.models import Carousel, Services, Whychooseuspix, Whychooseus, Homevideo, Blog, Comment, Category, Tags
from sajeksApp.forms import CommentForm
from django.db.models import aggregates, F, Count


# Create your views here.
def home(request):
    carousel = Carousel.objects.all()[0:3]
    services2 = Services.objects.all()
    service = Services.objects.all()[0:8]
    chooseus = Whychooseus.objects.all()[0:3]
    choosepix = Whychooseuspix.objects.first()
    homevideo = Homevideo.objects.first()

    blog = Blog.objects.all()[0:3]
    
    context ={
        'carousels':carousel,
        'services2':services2,
        'services':service,
        'chooses': chooseus,
        'choosepix':choosepix,
        'homevideos':homevideo,
        'blogs':blog
    }
    return render(request, 'sajeksApp/index.html', context)

def blog(request):
    blogs = Blog.objects.all()
    
    context ={
        'blogs':blogs
    }
    return render(request, 'sajeksApp/blog.html', context)



def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    recent_post = Blog.objects.all()
    tags = Tags.objects.all()

    categories = Category.objects.annotate(post_count = Count('posts') )
    
    top_level_comments = Comment.objects.filter(blog=blog, parent=None).order_by('-created_on')
    comment_count = Comment.objects.filter(blog=blog)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.blog = blog
            
            # Get the parent_id from the form
            parent_id = form.cleaned_data.get('parent')
            
            # Correctly handle the parent field
            if parent_id:
                # Retrieve the Comment instance using the parent_id
                parent_comment = get_object_or_404(Comment, id=parent_id)
                # Assign the retrieved instance to the parent field
                new_comment.parent = parent_comment

            new_comment.save()
            return redirect('blog_detail', blog_id=blog.id)
    else:
        form = CommentForm()
        
    context = {
        'blog': blog,
        'recent_posts': recent_post,
        'comments': top_level_comments,
        'form': form,
        'comment_count': comment_count.count(),
        'categories_count':categories,
        'tags':tags
    }
    return render(request, 'sajeksApp/blog-details.html', context)

def categories(request, category_id):
    category = Category.objects.get(name = category_id)
    get_blog = Blog.objects.filter(categories = category)

    context = {
        'blogs': get_blog
    }

    return render(request, 'sajeksApp/categories/category.html', context)

def tag(request, tag_id):
    tags = Tags.objects.get(name = tag_id)
    blog = Blog.objects.filter(tag =tags)
   
    context = {
       'blogs': blog
     }
    return render(request, 'sajeksApp/categories/tags.html', context)