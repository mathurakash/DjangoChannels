from .models import User_Profile
from django import forms
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=User_Profile
        fields=['first_name','last_name','email','phone','image']
        widgets={
            'first_name':forms.TextInput(attrs={"placeholder": "Enter First Name","class":"form-control"}),
            'last_name':forms.TextInput(attrs={ "placeholder": "Enter Last Name","class":"form-control"}),
            'email':forms.TextInput(attrs={"placeholder": "Enter Email Address","class":"form-control"}),
            'phone':forms.TextInput(attrs={ "placeholder": "Enter Phone Number","class":"form-control"}),
            
        }