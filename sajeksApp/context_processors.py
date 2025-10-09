# your_app/context_processors.py
from .forms import TestimonialForm

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