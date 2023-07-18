from django import forms
from django.forms import ModelForm
from django.contrib.postgres.forms import SplitArrayField
from .models import Hint, Insight

class HintForm(forms.Form):
    hint = forms.CharField(widget=forms.Textarea(attrs={'name':'hint', 'rows':5, 'cols': 30, 'placeholder': "Type your new hint..."}), label="New Hint:", min_length=8, max_length=300)
class InsightForm(forms.Form):
    insight = forms.CharField(widget=forms.Textarea(attrs={'name':'insight', 'rows':5, 'cols': 30, 'placeholder': "Type your new insight.."}), label="New Insight:", min_length=8, max_length=300)
class HintUpdateForm(ModelForm):
    class Meta:
        model = Hint
        fields = ['text']
    text = forms.CharField(widget=forms.Textarea(attrs={'name':'hint', 'rows':5, 'cols': 30, 'placeholder': "Update your hint..."}), label="Update your hint:", min_length=8, max_length=300)
class InsightUpdateForm(ModelForm):
    class Meta:
        model = Insight
        fields = ['text']
    text = forms.CharField(widget=forms.Textarea(attrs={'name':'insight', 'rows':5, 'cols': 30, 'placeholder': "Update your insight..."}), label="Update your insight:", min_length=8, max_length=300)