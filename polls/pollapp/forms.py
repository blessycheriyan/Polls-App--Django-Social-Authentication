from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from django.contrib.auth.models import User
from django.core import validators


from .models import Choice, Profile, newsletter
from django.forms import ModelForm


class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'

class userform(UserCreationForm):
    email = forms.EmailField(help_text='write your email', required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        mail = User.objects.filter(email=email)

        if mail:
             msg = "Email already registered"
             self.add_error("email", msg)

class userformedit(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]

from captcha.fields import CaptchaField

class CaptchaForm(forms.Form):
    captcha = CaptchaField()





class UserProfileForm(forms.ModelForm):


    phone = forms.CharField(validators=[validators.MaxLengthValidator(10)])


    class Meta:
        model = Profile
        fields = ['profile_pic', 'phone','country']


class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={

        "placeholder": "Type your email address"}))

    class Meta:
        model = newsletter
        fields = ['email']