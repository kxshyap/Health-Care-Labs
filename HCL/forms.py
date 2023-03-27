from django import forms
from .models import user_info,test_info,contact_info

# Create your models here.


class signupForm(forms.ModelForm):
    class Meta:
        model=user_info
        fields='__all__'

class testForm(forms.ModelForm):
    class Meta:
        model=test_info
        fields='__all__'

class contactForm(forms.ModelForm):
    class Meta:
        model=contact_info
        fields='__all__'



        