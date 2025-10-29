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
            existing_user = Subscribtion.objects.filter(email=email_to_check).first()
            
            if existing_user:
                
                if existing_user.is_active:
                    messages.warning(request, f'The email address "{email_to_check}" is already subscribed!')
                else:
                    existing_user.is_active =True
                    existing_user.save()
                    messages.success(request, f'Welcome back! Your subscription for "{email_to_check}" has been reactivated!')
                
                return_path = request.POST.get('next', reverse('home'))
                return redirect(return_path)
            else:   
                new_subscriber = sub_form.save(commit=False)
                new_subscriber.is_active = True
                new_subscriber.save()
                messages.success(request, 'Thank you for subscribing!')
                
        else:
            messages.error(request, 'Please ensure you enter a valid email address.') 
        return_path = request.POST.get('next', reverse('home'))
        return redirect(return_path)
    return redirect('home')   

