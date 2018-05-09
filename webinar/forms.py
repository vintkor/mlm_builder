from django import forms
from .models import Webinar


class WebinarUpdateForm(forms.ModelForm):

    class Meta:
        model = Webinar
        exclude = ('owner', 'is_moderate', 'slug',)
        widgets = {
            'active_start_date': forms.TextInput(attrs={'class': 'datetime'})
        }


class WebinarCreateForm(forms.ModelForm):

    class Meta:
        model = Webinar
        exclude = ('owner', 'is_moderate', 'slug',)
