# your_app/forms.py
from turtle import textinput
from django import forms
from .models import Blog, Comment, Contact, Subscribtion, Testimonial
from django import forms

class CommentForm(forms.ModelForm):
    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)
    class Meta:   
        # Exclude the parent field from automatic saving
        exclude = ('parent',) 
        model = Comment
        fields = ['full_name', 'email', 'website', 'content', 'img', 'parent']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email*'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Your Website (e.g., https://www.example.com)'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Comment*'}),
            'img': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Optional'})
        }

    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website and not (website.startswith('http://') or website.startswith('https://')):
            # Add the protocol if the user forgot it
            website = f'https://{website}'
        return website
class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search', 
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter search term'})
    )

class SubscribtionForm(forms.ModelForm):
    class Meta:
        model = Subscribtion
        fields = ['email'] 
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control h-100 bg-secondary', 
                'placeholder': 'Enter your e-mail',
                
            }),
        }

class ContactForm(forms.ModelForm):
    
    class Meta:   
        
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email*'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message*'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject*'}),
            
        }


class TestimonialForm(forms.ModelForm):
    # Overwrite the rating field to use RadioSelect, which works well with the custom star CSS
    rating = forms.IntegerField(
        label='Rate Your Experience (1 to 5 Stars)',
        widget=forms.RadioSelect(choices=[
            (1, '⭐'), 
            (2, '⭐⭐'), 
            (3, '⭐⭐⭐'), 
            (4, '⭐⭐⭐⭐'), 
            (5, '⭐⭐⭐⭐⭐')
        ]),
        initial=5,
    )

    class Meta:
        model = Testimonial
        fields = ['full_name', 'rating', 'message', 'image']
        
        # Add Bootstrap's default 'form-control' class to other fields
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Your Full Name'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Share your detailed experience here...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}), # File inputs need form-control
        }