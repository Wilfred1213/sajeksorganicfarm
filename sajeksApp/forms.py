# your_app/forms.py
from turtle import textinput
from django import forms
from .models import Blog, Comment
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

class CommentForm(forms.Form):
    query  = forms.CharField(label='Search', max_length=100, required=False,
            Widgets =forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter search term'}))
    
        