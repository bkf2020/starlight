from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.postgres.forms import SplitArrayField
from .models import Hint, Insight
from better_profanity import profanity
from django.contrib.staticfiles.storage import staticfiles_storage

profanity_loc = staticfiles_storage.path("profanity.txt")
profanity.load_censor_words_from_file(profanity_loc)

class HintForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        hint_text = cleaned_data.get("hint")
        if hint_text is not None and profanity.contains_profanity(hint_text):
            raise ValidationError("We think your hint contains profanity. Please remove the profanity and then submit again.")
        return cleaned_data
    hint = forms.CharField(widget=forms.Textarea(attrs={'name':'hint', 'rows':5, 'cols': 30, 'placeholder': "Type your new hint...", "class": "textarea textarea-bordered"}), label="New Hint:", min_length=8, max_length=300)
class InsightForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        insight_text = cleaned_data.get("insight")
        if insight_text is not None and profanity.contains_profanity(insight_text):
            raise ValidationError("We think your insight contains profanity. Please remove the profanity and submit again.")
        return cleaned_data
    insight = forms.CharField(widget=forms.Textarea(attrs={'name':'insight', 'rows':5, 'cols': 30, 'placeholder': "Type your new insight..", "class": "textarea textarea-bordered"}), label="New Insight:", min_length=8, max_length=300)
class HintUpdateForm(ModelForm):
    class Meta:
        model = Hint
        fields = ['text']
    def clean(self):
        cleaned_data = super().clean()
        hint = cleaned_data.get("text")
        if hint is not None and profanity.contains_profanity(hint):
            raise ValidationError("We think your hint contains profanity. Please remove the profanity and submit again.")
        return cleaned_data
    text = forms.CharField(widget=forms.Textarea(attrs={'name':'hint', 'rows':5, 'cols': 30, 'placeholder': "Update your hint...", "class": "textarea textarea-bordered"}), label="Update your hint:", min_length=8, max_length=300)
class InsightUpdateForm(ModelForm):
    class Meta:
        model = Insight
        fields = ['text']
    def clean(self):
        cleaned_data = super().clean()
        insight = cleaned_data.get("text")
        if insight is not None and profanity.contains_profanity(insight):
            raise ValidationError("We think your insight contains profanity. Please remove the profanity and submit again.")
        return cleaned_data
    text = forms.CharField(widget=forms.Textarea(attrs={'name':'insight', 'rows':5, 'cols': 30, 'placeholder': "Update your insight...", "class": "textarea textarea-bordered"}), label="Update your insight:", min_length=8, max_length=300)