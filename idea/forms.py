from django import forms
from .models import *

class AddIdeaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Idea
        fields = ['title', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'score']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }