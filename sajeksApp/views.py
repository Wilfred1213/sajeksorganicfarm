from itertools import count
from typing import Counter
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from sajeksApp.models import Carousel, Services,ProduceItem, Whychooseuspix, Team, Testimonial, Whychooseus,adminContact, About_us, Homevideo, Blog, Comment, Category, Tags
from sajeksApp.forms import CommentForm, SearchForm, Contact, SubscribtionForm, ContactForm, TestimonialForm
from sajeksApp.subscription import subscribe_handler
from sajeksApp.paginator import paginate_queryset
from django.db.models import aggregates, F, Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    contact = adminContact.objects.first()
    carousel = Carousel.objects.all()[0:3]
    services2 = Services.objects.all()
    service = Services.objects.all()[0:8]
    chooseus = Whychooseus.objects.all()[0:3]
    choosepix = Whychooseuspix.objects.first()
    # homevideo = Homevideo.objects.first()
    recent_videos = Homevideo.objects.all()[:3]
    produce_items = ProduceItem.objects.all()
    products = paginate_queryset(request, produce_items, items_per_page=8)
    
    user = request.user

    blog = Blog.objects.all()[0:3]
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    # message_count = Contact.objects.aggregate(msg = Count(msg_countig))

    # ONLY instantiate the form for rendering (NO POST logic here)
    subscribtion_form = SubscribtionForm()
    
    context ={
        'admincontact':contact,
        'carousels':carousel,
        'services2':services2,
        'services':service,
        'chooses': chooseus,
        'choosepix':choosepix,
        'homevideos':recent_videos,
        'blogs':blog,
        'sub_form': subscribtion_form,
        'produce_items': products,
        'message_count':message_count,
        'user':user
    }
    return render(request, 'sajeksApp/index.html', context)

def blog(request):
    blog_list = Blog.objects.all()
    blog_list = Blog.objects.all().order_by('-created_on') 

    # 2. Use the helper function (Refactored Logic)
    blogs = paginate_queryset(request, blog_list, items_per_page=9)

    subscribtion_form = SubscribtionForm()
    contact = adminContact.objects.first()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    context ={
        'admincontact':contact,
        'blogs':blogs,
        'sub_form':subscribtion_form,
        'message_count':message_count
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
            
            if parent_id:
                # Retrieve the Comment instance using the parent_id
                parent_comment = get_object_or_404(Comment, id=parent_id)
                # Assign the retrieved instance to the parent field
                new_comment.parent = parent_comment

            new_comment.save()
            redirect_url = f"{reverse('blog_detail', args=[blog.id])}#comment-form-section"
            return redirect(redirect_url)
            # return redirect('blog_detail', blog_id=blog.id)
    else:
        form = CommentForm()
    
    # search view
    search_blogs = None
    search_form = SearchForm(request.GET or None)     
    if request.method == 'GET' and search_form.is_valid():
        search_query = search_form.cleaned_data.get('query')
        if search_query:
            query_filter = Q(title__icontains=search_query)|Q(content__icontains=search_query) | Q(tag__name__icontains=search_query) | Q(content2__icontains=search_query) |Q(categories__name__icontains=search_query)
            search_blogs = Blog.objects.filter(query_filter).distinct()
        
    subscribtion_form = SubscribtionForm()
    contact = adminContact.objects.first()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    context = {
        'admincontact':contact,
        'blog': blog,
        'recent_posts': recent_post,
        'comments': top_level_comments,
        'form': form,
        'comment_count': comment_count.count(),
        'categories_count':categories,
        'tags':tags,
        'search_blog':search_blogs,
        'search_form':search_form,
        'sub_form': subscribtion_form,
        'message_count':message_count
        
    }
    return render(request, 'sajeksApp/blog-details.html', context)

def categories(request, category_id):
    category = Category.objects.get(name = category_id)
    get_blog = Blog.objects.filter(categories = category)

    blogs = paginate_queryset(request, get_blog, items_per_page=9)

    subscribtion_form = SubscribtionForm()
    contact = adminContact.objects.first()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()

    context = {
        'admincontact':contact,
        'blogs': blogs,
        'sub_form':subscribtion_form,
        'message_count':message_count
    }

    return render(request, 'sajeksApp/blog.html', context)

def tag(request, tag_id):
    tags = Tags.objects.get(name = tag_id)
    blog = Blog.objects.filter(tag =tags)

    blogs = paginate_queryset(request, blog, items_per_page=9)

    subscribtion_form = SubscribtionForm()
    contact = adminContact.objects.first()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
   
    context = {
       'blogs': blogs,
       'sub_form': subscribtion_form,
       'admincontact':contact,
       'message_count':message_count
     }
    return render(request, 'sajeksApp/blog.html', context)

def videos(request):
    
    homevideo = Homevideo.objects.all()
    contact = adminContact.objects.first()    
    paging = paginate_queryset(request, homevideo, items_per_page=9)
    subscribtion_form = SubscribtionForm()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    
    context = {
        'admincontact':contact,
        'homevideos':paging,
        'sub_form': subscribtion_form,
        'message_count':message_count
        
    }
    return render(request, 'sajeksApp/videos/videos.html', context)
    

def video_details(request, video_id):
    video = get_object_or_404(Homevideo, id = video_id)
    subscribtion_form = SubscribtionForm()
    contact = adminContact.objects.first()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    context = {
        'homevideos':video,
        'sub_form': subscribtion_form,
        'admincontact':contact,
        'message_count':message_count
    }
    
    return render(request, 'sajeksApp/videos/video_detail.html', context)

def service(request):
    service = Services.objects.all()
    chooseus = Whychooseus.objects.all()[0:3]
    choosepix = Whychooseuspix.objects.first()
    subscribtion_form = SubscribtionForm()
    recent_videos = Homevideo.objects.all()[:3]

    produce_items = ProduceItem.objects.all()
    products = paginate_queryset(request, produce_items, items_per_page=8)

    contact = adminContact.objects.first()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    context = {
        'services':service,
        'chooses': chooseus,
        'choosepix':choosepix,
        'sub_form': subscribtion_form,
        'produce_items':products,
        'homevideos':recent_videos,
        'admincontact':contact,
        'message_count':message_count
    }
    return render(request, 'sajeksApp/services.html', context)

def about(request):
    about = About_us.objects.first()
    subscribtion_form = SubscribtionForm()
    team = Team.objects.all()
    
    chooseus = Whychooseus.objects.all()[0:3]
    choosepix = Whychooseuspix.objects.first()

    produce_items = ProduceItem.objects.all()
    products = paginate_queryset(request, produce_items, items_per_page=50)
    contact = adminContact.objects.first()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    context={
        'chooses':chooseus,
        'choosepix':choosepix,
        'abouts':about,
        'admincontact':contact,
        'sub_form': subscribtion_form,
        'produce_items': products,
        'teams':team,
        'message_count':message_count
    }
    return render(request, 'sajeksApp/about.html', context)


def produce_list_view(request):
    produce_items = ProduceItem.objects.all()
    blog = Blog.objects.all()
    subscribtion_form = SubscribtionForm()
    products = paginate_queryset(request, produce_items, items_per_page=50)
    contact = adminContact.objects.first()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    context = {
        'admincontact':contact,
        'produce_items': products, 
        'blogs':blog,
        'sub_form': subscribtion_form,
        'message_count':message_count
    }
    return render(request, 'sajeksApp/product_list.html', context)

def contact(request):
    admin_info = adminContact.objects.first()
    form = ContactForm(request.POST)

    if request.method == 'POST':
        if form.is_valid:
            form.save()
            messages.info(request, 'Thank you for contacting us. We will get back to you shortly.')
            return redirect('contact')
        messages.error(request, 'Sorry your input is not correct')
        return redirect('contact')
    form = ContactForm()

    produce_items = ProduceItem.objects.all()
    products = paginate_queryset(request, produce_items, items_per_page=8)

    subscribtion_form = SubscribtionForm()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    

    context={
        'form':form,
        'produce_items': products,
        'admincontact':admin_info,
        'sub_form': subscribtion_form,
        'message_count':message_count
    }
        
    return render(request,'sajeksApp/contact.html', context )

def testimonial(request):
    testimony = Testimonial.objects.all()
    blog = Blog.objects.all()[0:3]
    recent_videos = Homevideo.objects.all()[:3]
    contact = adminContact.objects.first()
    testimonial_pagination = paginate_queryset(request, testimony, items_per_page=12)
    subscribtion_form = SubscribtionForm()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    context ={
        'admincontact':contact,
        'testimonys':testimonial_pagination,
        'blogs':blog,
        'homevideos':recent_videos,
        'sub_form': subscribtion_form,
        'message_count':message_count
    }
    return render(request,'sajeksApp/testimonials.html', context )


def submit_testimonial_view(request):
    contact = adminContact.objects.first()
    """Handles the submission of the testimonial form via AJAX or standard POST."""
    
    # Check if the request is AJAX (from the JavaScript fetch call)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES) 
        
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.is_approved = False 
            testimonial.save()
            
            if is_ajax:
                # SUCCESS for AJAX: Return JSON instructing the frontend to proceed
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you! Your testimonial is submitted for review.',
                }, status=200)
            else:
                # SUCCESS for standard form submission (e.g., if JS fails)
                messages.success(request, 'Thank you! Your testimonial has been submitted successfully and is pending review.')
                return redirect(reverse('testimonial')) 
                
        else:
            # ERROR Handling
            if is_ajax:
                # ERROR for AJAX: Return JSON containing the errors
                # This allows the JavaScript to display field-specific errors
                return JsonResponse({
                    'success': False,
                    'errors': form.errors.get_json_data(),
                    'message': 'Please correct the errors in the form.'
                }, status=400) # Use 400 status code for Bad Request
            else:
                # ERROR for standard form submission: Render the page with errors shown
                messages.error(request, 'There was an error in your submission. Please correct the highlighted fields.')
                # Note: This branch is usually for non-AJAX forms, but kept for completeness
                return render(request, 'sajeksApp/testimonial_form.html', {'form': form})
    
    # Handle GET request (e.g., direct navigation to the form URL)
    else:
        form = TestimonialForm()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    
    subscribtion_form = SubscribtionForm()
    
    context = {
        'form': form,
        'admincontact':contact,
        'message_count':message_count,
        'sub_form':subscribtion_form
    }
    return render(request, 'sajeksApp/testimonial_form.html', context)

def contact_list(request):
    contacts = Contact.objects.all().order_by('-posted_on')
    unread_count= Contact.objects.filter(status = True).count()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    subscribtion_form = SubscribtionForm()
    context ={
        'contacts':contacts,
        'unread_count':unread_count,
        'message_count':message_count,
        'sub_form':subscribtion_form
    }
    return render(request, 'sajeksApp/contact_list.html', context)

def contact_detail(request, contact_id):
    contactid = get_object_or_404(Contact, pk = contact_id)
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    
    subscribtion_form = SubscribtionForm()
    
    context = {
        'msg':contactid,
        'message_count':message_count,
        'sub_form':subscribtion_form
              
    }
    return render(request, 'sajeksApp/contact_detail.html', context)

def mark_as_read(request, contact_id):
    contactid = get_object_or_404(Contact, pk = contact_id)
    
    if contactid.status == True:
        contactid.status = False
        contactid.save()
        return redirect(reverse('contact_detail', args=[contact_id]))
      
def delete_contact(request, contact_id):
    user = request.user
    contactid = get_object_or_404(Contact, pk = contact_id)
    
    if user.is_superuser | user.is_staff:
        contactid.delete()
        return redirect('contact_list')
        
        
