from django import forms
from django.contrib.postgres.forms import SplitArrayField

class HintForm(forms.Form):
    hint = forms.CharField(widget=forms.Textarea(attrs={'name':'hint', 'rows':1, 'cols':60}), label="New Hint:", min_length=8, max_length=300)
class InsightForm(forms.Form):
    insight = forms.CharField(widget=forms.Textarea(attrs={'name':'insight', 'rows':1, 'cols':60}), label="New Insight:", min_length=8, max_length=300)