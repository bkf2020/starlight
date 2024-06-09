from django import forms

class ProblemStatusForm(forms.Form):
    STATUS_CHOICES = (
        ('NS', 'Not started'),
        ('IP', 'In progress'),
        ('NHS', 'Needed help to solve'),
        ('SO', 'Solved')
    )
    status = forms.ChoiceField(label='', widget=forms.Select(attrs={'class': 'statusForm select select-bordered bg-inherit border-black focus:border-black focus:outline-black'}), choices=STATUS_CHOICES)
    problem_id = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class': 'problemId'}))
