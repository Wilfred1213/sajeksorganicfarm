from itertools import count
from typing import Counter
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from sajeksApp.models import Carousel, Services,ProduceItem, Whychooseuspix, Team, Testimonial, Whychooseus,adminContact, Gallary, About_us, Homevideo, Blog, Comment, Category, Tags, Subscribtion
from sajeksApp.forms import CommentForm, SearchForm, NewsletterForm, Contact, SubscribtionForm, ContactForm, TestimonialForm
from sajeksApp.subscription import subscribe_handler
from sajeksApp.paginator import paginate_queryset
from django.db.models import aggregates, F, Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required # Important for security
from django.core.mail import EmailMessage
from django.conf import settings
from sajeksApp.context_processors import build_unsubscribe_link


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

    produce_items = ProduceItem.objects.all()
    products = paginate_queryset(request, produce_items, items_per_page=8)
    context ={
        'admincontact':contact,
        'blogs':blogs,
        'sub_form':subscribtion_form,
        'message_count':message_count,

        'produce_items':products
    }
    return render(request, 'sajeksApp/blog.html', context)



def blog_detail(request, blog_id):
    try:
        blog = get_object_or_404(Blog, id=blog_id)
    except Blog.DoesNotExist:
        messages.info(request, 'This blog does not exist')
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
    try:
        category = Category.objects.get(name = category_id)
    except Category.DoesNotExist:
        messages.info(request, 'This Category does not exist')
    get_blog = Blog.objects.filter(categories = category)

    blogs = paginate_queryset(request, get_blog, items_per_page=9)

    subscribtion_form = SubscribtionForm()
    contact = adminContact.objects.first()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    
    produce_items = ProduceItem.objects.all()
    products = paginate_queryset(request, produce_items, items_per_page=8)

    context = {
        'admincontact':contact,
        'blogs': blogs,
        'sub_form':subscribtion_form,
        'message_count':message_count,
        'produce_items':products
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
    
    produce_items = ProduceItem.objects.all()
    products = paginate_queryset(request, produce_items, items_per_page=8)
   
    context = {
       'blogs': blogs,
       'sub_form': subscribtion_form,
       'admincontact':contact,
       'message_count':message_count,
       'produce_items':products
     }
    return render(request, 'sajeksApp/blog.html', context)

def videos(request):
    
    homevideo = Homevideo.objects.all()
    contact = adminContact.objects.first()    
    paging = paginate_queryset(request, homevideo, items_per_page=9)
    subscribtion_form = SubscribtionForm()
    
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()
    
    produce_items = ProduceItem.objects.all()
    products = paginate_queryset(request, produce_items, items_per_page=8)
    context = {
        'admincontact':contact,
        'homevideos':paging,
        'sub_form': subscribtion_form,
        'message_count':message_count,
        'produce_items':products
        
    }
    return render(request, 'sajeksApp/videos/videos.html', context)
    

def video_details(request, video_id):
    try:
        video = get_object_or_404(Homevideo, id = video_id)
    except Homevideo.DoesNotExist:
        messages.error(request, 'This video does not exist anymore')
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

    produce_items = ProduceItem.objects.all()[:8]
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
    blog = Blog.objects.all()[:3]
    subscribtion_form = SubscribtionForm()
    products = paginate_queryset(request, produce_items, items_per_page=32)
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
    blog = Blog.objects.all()[0:3]
    form = ContactForm(request.POST)

    if request.method == 'POST':
        if form.is_valid:
            form.save()
            messages.info(request, 'Thank you for contacting us. We will get back to you shortly. Thank you! 👋')
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
        'blogs':blog,
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
    try:
        contactid = get_object_or_404(Contact, pk = contact_id)
    except Contact.DoesNotExist:
        messages.error(request, 'This contact does not exist anymore')
        return redirect('contact_list')
    
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
    try:
        contactid = get_object_or_404(Contact, pk = contact_id)
    except Contact.DoesNotExist:
        messages.error(request, 'already mark as read')
    if contactid.status == True:
        contactid.status = False
        contactid.save()
        return redirect(reverse('contact_detail', args=[contact_id]))
      
def delete_contact(request, contact_id):
    user = request.user
    contactid = get_object_or_404(Contact, pk = contact_id)
    
    if user.is_superuser | user.is_staff:
        contactid.delete()
        messages.info(request, f'You successfully deleted {contactid.name} message')
        return redirect('contact_list')
    messages.error(request, 'You dont have permission to delete this message!')
    return redirect('contact_list')
    
def gallery(request):
    gallerys =  Gallary.objects.all()
    msg_countig = Contact.objects.filter(status =True)
    message_count = msg_countig.count()

    subscribtion_form = SubscribtionForm()

    context = {
        'gallery':gallerys,
        'sub_form':subscribtion_form,
        'message_count':message_count,
    }
        
    return render(request, 'sajeksApp/gallery.html', context)  


@staff_member_required
def send_newsletter_view(request):
    form = NewsletterForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        subject = form.cleaned_data.get('subject')
        # Use HTML for the body if you plan on complex formatting later, 
        # but for now, we'll keep it simple:
        original_body = form.cleaned_data.get('body')
        
        # 1. Fetch ALL active Subscriber OBJECTS
        subscribers = Subscribtion.objects.filter(is_active=True)
        
        if not subscribers.exists():
            messages.warning(request, "No active subscribers found to send the newsletter.")
            return redirect('send_newsletter_view')

        # 2. Prepare the email list
        emails = []
        
        for subscriber in subscribers:
            # Build the unique unsubscribe link for this user
            unsubscribe_link = build_unsubscribe_link(request, subscriber)
            
            # Append the unsubscribe footer to the email body
            footer = (
                "\n\n-----------------------------------\n"
                f"You are receiving this because you subscribed to our list.\n"
                f"To instantly unsubscribe, click here:\n"
                f"{unsubscribe_link}"
            )
            
            full_body = original_body + footer
            
            # Create the EmailMessage instance
            email_message = EmailMessage(
                subject=subject,
                body=full_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email], # Use the email from the object
                # bcc=[settings.ADMIN_EMAIL], 
            )
            emails.append(email_message)

        # 3. Send emails in bulk for efficiency (remains the same)
        try:
            # Note: We still use 'connection = None' for simplicity in this example.
            connection = None 
            sent_count = 0
            
            sent_count = connection.send_messages(emails) if connection else sum(e.send() for e in emails)

            messages.success(request, f"Newsletter sent successfully to {sent_count} subscribers! 🎉")
            return redirect('send_newsletter_view')

        except Exception as e:
            messages.error(request, f"An error occurred while sending the newsletter: {e}")
            
    context = {
        'form': form, 
        'subscribers_count': Subscribtion.objects.filter(is_active=True).count()
    }
    return render(request, 'sajeksApp/admin/newsletter_form.html', context)

def unsubscribe_view(request, token):
    try:
        # 1. Look up the subscriber using the unique token
        subscriber = Subscribtion.objects.get(token=token, is_active=True)
        
        # 2. Deactivate the subscriber
        subscriber.is_active = False
        subscriber.save()
        
        # 3. Success message for the user
        messages.success(request, f"You have been successfully unsubscribed ({subscriber.email}). We're sorry to see you go!")
        
    except Subscribtion.DoesNotExist:
        # If token is invalid or already unsubscribed
        messages.error(request, "This link is invalid or you are already unsubscribed.")
        
    # Redirect to a simple thank you page or the homepage
    return redirect('home') # Use your actual homepage URL name