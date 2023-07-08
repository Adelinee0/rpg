from django import forms
from .models import Advert, Response

class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = [
            'title',
            'category',
            'text',
        ]

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'text'
        ]