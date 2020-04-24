from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Message, Conversation


class SignupForm(UserCreationForm):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UpdateForm(forms.Form):
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    gender = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('gender', 'phone', 'birth_date', 'username', 'first_name', 'last_name', 'email')


class SigninForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)


class MessageForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = Message
        fields = ('content',)


class ConversationForm(forms.Form):

    class Meta:
        model = Conversation
