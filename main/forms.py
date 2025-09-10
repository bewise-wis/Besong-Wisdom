from django import forms
from django.core.exceptions import ValidationError
import time

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
            'required': 'required'
        }),
        required=True,
        error_messages={'required': 'Please enter your name'}
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email',
            'required': 'required'
        }),
        required=True,
        error_messages={'required': 'Please enter your email', 'invalid': 'Please enter a valid email address'}
    )
    subject = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject',
            'required': 'required'
        }),
        required=True,
        error_messages={'required': 'Please enter a subject'}
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your Message',
            'rows': 5,
            'required': 'required'
        }),
        required=True,
        error_messages={'required': 'Please enter your message'}
    )
    timestamp = forms.CharField(
        widget=forms.HiddenInput(), 
        required=False
    )
    
    def clean_timestamp(self):
        timestamp = self.cleaned_data.get('timestamp')
        if timestamp:
            elapsed = time.time() - float(timestamp)
            if elapsed < 3:  # Less than 3 seconds to submit is likely a bot
                raise ValidationError('Form submitted too quickly. Please try again.')
        return timestamp
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 10:
            raise ValidationError('Message is too short. Please provide more details.')
        return message