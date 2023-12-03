from django import forms
from ckeditor.widgets import CKEditorWidget 
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    """Form for adding a new topic."""
    
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    """A form for adding new entries to the learning log."""

    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': CKEditorWidget(),
        }
