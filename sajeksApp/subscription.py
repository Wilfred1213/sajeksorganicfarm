from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from .forms import SubscribtionForm 
from .models import Subscribtion

def subscribe_handler(request):
    
    if request.method == 'POST':
        sub_form = SubscribtionForm(request.POST)
        
        if sub_form.is_valid():
            email_to_check = sub_form.cleaned_data.get('email')
            if Subscribtion.objects.filter(email=email_to_check).exists():
                messages.warning(request, f'The email address "{email_to_check}" is already subscribed!')
            else:
                sub_form.save()
                messages.success(request, 'Thank you for subscribing!')
        
        else:
            messages.error(request, 'Please ensure you enter a valid email address.') 
        return_path = request.POST.get('next', reverse('home'))
        return redirect(return_path)
    return redirect('home')   
