from django import forms

from models import SubjectPost
from models import Subject, Subcategory
from tinymce.widgets import AdminTinyMCE
from utility.utility import clean_file
from django.db.models.query_utils import Q
from operator import or_


class SubjectPostCreationFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
                           label='')
    
    show_files = True
    show_preview = True
    preview_url = "/preview_subjectpost/"

    class Meta:
        model = SubjectPost
        fields = ('name', 'subcategory', 'subject', 'file')
        
    def __init__(self, *args, **kwargs):
        super(SubjectPostCreationFormAdmin, self).__init__(*args, **kwargs)
        user = self.current_user
        if user.status is 2:
          self.fields['subject'].queryset = user.subjects.all()
          
          self.fields['subcategory'].queryset = Subcategory.objects.filter(reduce(or_, [Q(subject=s) for s in user.subjects.all()]))
        
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def clean_subject(self):
        subject = self.cleaned_data.get("subject")
        subcategory = self.cleaned_data.get("subcategory")
        if subcategory != None and subject != None and subject != subcategory.subject:
            raise forms.ValidationError("This should be empty or same subject as the subcategory")
        if subcategory == None and subject == None:
            raise forms.ValidationError("This should be not be empty")
        return self.cleaned_data.get("subject")
    
    def save(self, commit=True):
        post = super(SubjectPostCreationFormAdmin, self).save(commit=False)
        post.author = self.current_user
        post.text = self.cleaned_data['text']
        if commit:
            post.save()
        return post


class SubjectPostChangeFormAdmin(forms.ModelForm):
    text = forms.CharField(widget=AdminTinyMCE(attrs={'cols': 80, 'rows': 30}),
                           label='')
    show_files = True
    show_preview = True
    preview_url = "/preview_subjectpost/"

    class Meta:
        model = SubjectPost
        fields = ('name', 'file', 'subject', 'subcategory')

    def __init__(self, *args, **kwargs):
        initial = {
          'text': self.text_initial
        }
        kwargs['initial'] = initial
        super(SubjectPostChangeFormAdmin, self).__init__(*args, **kwargs)
        user = self.current_user
        if user.status is 2:
          self.fields['subject'].queryset = user.subjects.all()
          
          self.fields['subcategory'].queryset = Subcategory.objects.filter(reduce(or_, [Q(subject=s) for s in user.subjects.all()]))
          

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file
      
      
    def clean_subject(self):
        subject = self.cleaned_data.get("subject") if "subject" in self.changed_data else self.instance.subject
        subcategory = self.cleaned_data.get("subcategory") if "subcategory" in self.changed_data else self.instance.subcategory
        if subcategory != None and subject != None and subject != subcategory.subject:
            raise forms.ValidationError("This should be empty or same subject as the subcategory")
        if subcategory == None and subject == None:
            raise forms.ValidationError("This should be not be empty")
        return self.cleaned_data.get("subject")

    def save(self, commit=True):
        post = super(SubjectPostChangeFormAdmin, self).save(commit=False)
        post.text = self.cleaned_data['text']
        if commit:
            post.save()
        return post


class SubcategoryCreationFormAdmin(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ('name', 'file','subject',)
        
    def __init__(self, *args, **kwargs):
        super(SubcategoryCreationFormAdmin, self).__init__(*args, **kwargs)
        user = self.current_user
        if user.status is 2:
          self.fields['subject'].queryset = user.subjects.all()
          
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(SubcategoryCreationFormAdmin, self).save(commit=False)
        uploaded_file.author = self.current_user
        if commit:
            uploaded_file.save()
        return uploaded_file


class SubcategoryChangeFormAdmin(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ('name', 'file','subject')
    
    def __init__(self, *args, **kwargs):
        super(SubcategoryChangeFormAdmin, self).__init__(*args, **kwargs)
        user = self.current_user
        if user.status is 2:
          self.fields['subject'].queryset = user.subjects.all()

    
    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        error = clean_file(uploaded_file, image=True)
        if error:
            raise forms.ValidationError(error)
        return uploaded_file

    def save(self, commit=True):
        uploaded_file = super(SubcategoryChangeFormAdmin, self).save(commit=False)
        if commit:
            uploaded_file.save()
        return uploaded_file
