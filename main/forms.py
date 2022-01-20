from django import forms

from main.models import Document, Section


class DocumentForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Введите название отдела'}))
    doc_path = forms.FileField(widget=forms.FileInput(attrs={'class': 'form__input', 'accept':".pdf"}), required=False)
    section = forms.ModelChoiceField(queryset=Section.objects.all())
    note =forms.CharField(widget=forms.Textarea(attrs={'class': 'form__textarea'}))

    class Meta:
        model = Document
        fields = ('status', 'name', 'doc_path', 'section', 'note',)

