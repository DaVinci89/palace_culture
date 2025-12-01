from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'short_description', 'event_type',
            'start_date', 'end_date', 'location', 'price', 'max_participants',
            'image', 'is_featured'
        ]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class EventFilterForm(forms.Form):
    event_type = forms.ChoiceField(
        choices=[('', 'Всі типи')] + Event.EVENT_TYPES,
        required=False,
        label='Тип події'
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Від дати'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='До дати'
    )