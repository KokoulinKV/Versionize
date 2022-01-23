from django import forms

from main.models import Document, Section, Project, Company
from user.models import User


class DocumentForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form__input',
                                      'placeholder': 'Введите имя документа'}))
    doc_path = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form__input',
                                                                             'accept': ".pdf"}))
    section = forms.ModelChoiceField(queryset=Section.objects.all())
    note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form__textarea'}))

    class Meta:
        model = Document
        fields = ('status', 'name', 'doc_path', 'section', 'note',)


class AddSectionForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all().order_by('code'))
    abbreviation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input',
                                                                 'placeholder': 'Введите шифр раздела'}))
    company = forms.ModelChoiceField(queryset=Company.objects.all().order_by('name'))
    name = forms.CharField(widget=forms.Textarea(attrs={'class': 'form__textarea',
                                                        'placeholder': 'Введите полное наименование раздела'}))

    class Meta:
        model = Section
        fields = ('project', 'abbreviation', 'company', 'name')


class CreateProjectForm(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input',
                                                         'placeholder': 'Введите шифр проекта'}))
    name = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form__input',
                                     'placeholder': 'Введите Наименование объекта'}))

    admin = forms.ModelChoiceField(queryset=User.objects.filter(usercompanyinfo__chief_project_engineer=True))
    exp_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date',
                                                                             'class': "form__input"}))

    class Meta:
        model = Project
        fields = ('code', 'name', 'project_type', 'admin', 'exp_date')
