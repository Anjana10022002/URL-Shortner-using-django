from django import forms
from .models import URLShortner

class URLForm(forms.ModelForm):
    class Meta:
        model = URLShortner
        fields = ["title", "url"]