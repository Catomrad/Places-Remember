from django import forms
from .models import Memory


class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ['title', 'description']

    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())
