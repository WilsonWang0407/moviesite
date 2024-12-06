from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class FeedbackForm(forms.Form):
    OPTIONS = (('general feedback', 'General Feedback'), ('info change', 'Information Correction for a Movie'), ('add movie', 'Request to Add a Movie'), ('other', 'Other'))
    category = forms.ChoiceField(choices=OPTIONS, required=True)
    message = forms.CharField(widget=forms.Textarea, max_length=1000, required=True)

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}), max_length=1000, required=True)