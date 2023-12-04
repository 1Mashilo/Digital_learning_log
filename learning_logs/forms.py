from django import forms
from ckeditor.widgets import CKEditorWidget 
from .models import Topic, Entry
from bleach import clean

class TopicForm(forms.ModelForm):
    """Form for adding a new topic."""
    
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):

    def clean_text(self):
        text = self.cleaned_data['text']
        return clean(text, tags=[], strip=True)

    class Meta:
        model = Entry
        fields = ['text']
        widgets = {
            'text': CKEditorWidget(),
        }

