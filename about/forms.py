from django import forms
from .models import ContactFormSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormSubmission
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-ukraine-blue',
                'placeholder': 'Ваше ім\'я'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-ukraine-blue',
                'placeholder': 'Ваш email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-ukraine-blue',
                'placeholder': 'Ваш телефон'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-ukraine-blue',
                'placeholder': 'Тема повідомлення'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-ukraine-blue',
                'placeholder': 'Ваше повідомлення...',
                'rows': 5
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not any(char.isdigit() for char in phone):
            raise forms.ValidationError('Будь ласка, введіть коректний номер телефону')
        return phone