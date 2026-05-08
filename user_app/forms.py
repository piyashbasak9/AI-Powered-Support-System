from django import forms
from django.conf import settings

class AskQuestionForm(forms.Form):
    query = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        max_length=5000,
        required=True
    )
    file = forms.FileField(required=False)
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and file.size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise forms.ValidationError(f"File too large. Max {settings.MAX_FILE_SIZE_MB}MB")
        return file