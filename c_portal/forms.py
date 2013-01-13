from django import forms

from c_portal.models import *


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'abstract', 'body')


class SelectProjectForm(forms.Form):
    projects = forms.ModelMultipleChoiceField(queryset=Project.objects.all())


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'abstract', 'members')


class ArticleProjectsForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('project',)


class JoinProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',)


class AddTagForm(forms.Form):
    name = forms.CharField(max_length=255)


class AboutmeForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('aboutme',)
        widgets = {
                'aboutme': forms.Textarea(attrs={'class': 'input-block-level'}),
                }


class AbstractForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('abstract',)
        widgets = {
                'abstract': forms.Textarea(attrs={'class': 'input-block-level'}),
                }

