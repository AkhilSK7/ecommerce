from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from shop.models import Category,Product
class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2','email']

class LoginForm(forms.Form):
    username=forms.CharField(max_length=30)
    password=forms.CharField(max_length=30,widget=forms.PasswordInput)

class AddproductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','image','description','price','stock','category']

class AddcategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields="__all__"

class AddstockForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['stock']