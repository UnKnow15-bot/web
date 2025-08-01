from django import forms
from .models import Contact, Task


class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact 
        fields=['name', 'email', 'message']
 