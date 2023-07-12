from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Profile

class SignUpForm(UserCreationForm):
    #email = forms.EmailField(label="Email")
    #first_name = forms.CharField(label="Имя")
    #last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
class CustomSignupForm(SignUpForm):
    def save(self, request):
        user = super().save(request)
        return user


class CodeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'code_of_confirm'
        ]