from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'description', 'image_file', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }
