# your_app/context_processors.py
from .forms import TestimonialForm

from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site # Import this to get the domain safely

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