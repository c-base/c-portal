from django import forms

from shoutbox.models import *


class AddShoutForm(forms.ModelForm):
    class Meta:
        model = Shout
        fields = ('shout',)
        widgets = {
                'shout': forms.TextInput(attrs={'class': 'input-block-level'}),
                }
