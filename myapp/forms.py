from django import forms
from .models import *

class signupForm(forms.ModelForm):
    class Meta:
        model=signupmaster
        fields='__all__'

class updateForm(forms.ModelForm):
    class Meta:
        model=signupmaster
        fields=['firstname','lastname','username','password','city','state','mobile']
    
class notesForm(forms.ModelForm):
    class Meta:
        model=mynotes
        fields='__all__'

class feedbackForm(forms.ModelForm):
    class Meta:
        model=feedback
        fields='__all__'