# your_app/context_processors.py
from .forms import TestimonialForm

from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site # Import this to get the domain safely

from django.db.models import Q # Import Q objects for complex lookups
from .models import ProduceItem # Assuming this is your product model



def testimonial_form_processor(request):
    """Makes TestimonialForm available globally."""
    # We only create a BOUND form if the user just submitted it
    # We check for 'full_name' as a proxy for form submission
    if request.method == 'POST' and 'full_name' in request.POST:
         return {'testimonial_form': TestimonialForm(request.POST, request.FILES)}
    
    # Otherwise, return a fresh, unbound form
    return {'testimonial_form': TestimonialForm()}

# --- Add this to TEMPLATES in settings.py ---
# 'your_app.context_processors.testimonial_form_processor',



def build_unsubscribe_link(request, subscriber):
    """Constructs the absolute unsubscribe link for a given subscriber."""
    
    # Safely get the current site's domain and protocol
    current_site = get_current_site(request)
    domain = current_site.domain
    protocol = 'https' if request.is_secure() else 'http'
    
    # Build the relative URL using the token
    relative_url = reverse('unsubscribe_view', kwargs={'token': subscriber.token})
    
    # Construct the full absolute URL
    return f"{protocol}://{domain}{relative_url}"



# sajeksApp/context_processors.py


def global_products(request):
    """
    Makes a list of available produce items globally available in the template context.
    """
    
    # Check for a search query (q) parameter
    query = request.GET.get('q')
    
    # Start with all available items
    items = ProduceItem.objects.filter(is_available=True)
    
    # If a search query is present, filter the results.
    # Note: This means the search bar will work on every page where the products are displayed!
    if query:
        items = items.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        ).distinct()

    # The key in the dictionary becomes the variable name in your templates
    return {
        'global_produce_items': items,
        'search_query': query if query else '' # Optionally expose the query
    }