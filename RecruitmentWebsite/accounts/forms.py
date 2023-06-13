from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


# customise UserCreationForm to add email field
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        def save(self, commit=True):
            """clean 'email' data and save user email to the user"""
            user = super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user

# this form interacts with the profile model to let users update their profile
class UserProfileForm(forms.ModelForm):
    resume = forms.FileField(error_messages={'required': 'Please upload a non-empty file.'})
    email = forms.EmailField()
    phone = forms.CharField(required=False)
    image = forms.ImageField()
    username = forms.CharField()
    fullname = forms.CharField(label='Full Name')

    class Meta:
        model = Profile
        fields = ['bio', 'image', 'resume', 'username', 'fullname', 'email', 'phone']