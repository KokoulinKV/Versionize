from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from main.models import Document, Section, Project, Company, RemarksDocs
from user.models import User


class DocumentForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form__input',
                                      'placeholder': 'Введите имя документа'})
    )
    doc_path = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form__input',
                                      'accept': ".pdf"})
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all()
    )
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form__textarea'})
    )

    class Meta:
        model = Document
        fields = ('status', 'name', 'doc_path', 'section', 'note',)


class AddSectionForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all().order_by('code')
    )
    abbreviation = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form__input',
                                      'placeholder': 'Введите шифр раздела'})
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.all().order_by('name')
    )
    name = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form__textarea',
                                     'placeholder': 'Введите полное наименование раздела'})
    )

    class Meta:
        model = Section
        fields = ('project', 'abbreviation', 'company', 'name',)


class CreateProjectForm(forms.ModelForm):
    code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form__input',
                                      'placeholder': 'Введите шифр проекта'})
    )
    name = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form__input',
                                     'placeholder': 'Введите Наименование объекта'})
    )

    admin = forms.ModelChoiceField(
        queryset=User.objects.filter(usercompanyinfo__chief_project_engineer=True)
    )
    exp_date = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'date',
                                      'class': "form__input"})
    )

    class Meta:
        model = Project
        fields = ('code', 'name', 'project_type', 'admin', 'exp_date')

class AddRemarkDocProjectForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form__input',
                                      'placeholder': 'Введите имя документа'})
    )
    to_project = forms.ModelChoiceField(
        queryset=Project.objects.filter(
            id__in=Section.objects.filter(
                id__in=Document.objects.all().values('section_id')
            ).values('project_id')
        )
    )
    doc_path = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form__input'})
    )

    class Meta:
        model = RemarksDocs
        fields = ('name','to_project','doc_path',)



class AddRemarkDocSectionForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form__input',
                                      'placeholder': 'Введите имя документа'})
    )
    to_section = forms.ModelChoiceField(
        queryset=Section.objects.filter(id__in=Document.objects.all().values('section_id'))
    )
    doc_path = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form__input'})
    )
    
    def save(self, commit=True):
        remark = super(AddRemarkDocSectionForm, self).save()
        last_doc_in_section_id =Document.objects.filter(section=remark.to_section).values('id').latest('created_at')
        get_remark = RemarksDocs.objects.filter(id=remark.id)
        get_remark.update(to_document=last_doc_in_section_id['id'])
        return remark

    class Meta:
        model = RemarksDocs
        fields = ('name','to_section','doc_path',)


class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2',)

    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(user, *args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form__input'

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


