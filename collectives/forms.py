from django import forms
from .models import Collective

class CollectiveForm(forms.ModelForm):
    class Meta:
        model = Collective
        fields = [
            'name', 'collective_type', 'age_group', 'description', 'short_description',
            'leader', 'leader_photo', 'leader_description', 'schedule', 'image', 'youtube_url', 'rating'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'leader_description': forms.Textarea(attrs={'rows': 3}),
            'schedule': forms.Textarea(attrs={'rows': 3}),
        }

class CollectiveFilterForm(forms.Form):
    collective_type = forms.ChoiceField(
        choices=[('', 'Всі типи')] + Collective.COLLECTIVE_TYPES,
        required=False,
        label='Тип колективу'
    )
    age_group = forms.ChoiceField(
        choices=[('', 'Всі вікові групи')] + Collective.AGE_GROUPS,
        required=False,
        label='Вікова група'
    )