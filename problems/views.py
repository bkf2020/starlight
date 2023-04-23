from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from .models import Problem, Hint, Insight, HintCluster
from .forms import HintForm, InsightForm

# Create your views here.

def list(request):
    query = request.GET.get('search')
    if query is None or query == "":
        problems = Problem.objects.all().order_by("-id")
    else:
        problems = Problem.objects.filter(name__search=query).order_by("-id")
    paginator = Paginator(problems, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'full_path': request.get_full_path()
    }
    return render(request, 'problems/list.html', context)

# TODO: redirect urls for all these views

class HintUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Hint
    fields = ['text']
    template_name_suffix = '_update_form'
    def test_func(self):
        return self.request.user.username == self.get_object().username

class InsightUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Insight
    fields = ['text']
    template_name_suffix = '_update_form'
    def test_func(self):
        return self.request.user.username == self.get_object().username

class HintDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Hint
    fields = ['text']
    template_name_suffix = '_confirm_delete'
    def test_func(self):
        return self.request.user.username == self.get_object().username

class InsightDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Insight
    fields = ['text']
    template_name_suffix = '_confirm_delete'
    def test_func(self):
        return self.request.user.username == self.get_object().username

def problem(request, index):
    if(Problem.objects.filter(id=index).count() == 0):
        return redirect('/problems/')
    hint_form = HintForm()
    insight_form = InsightForm()
    if request.method == 'POST':
        # TODO: at most 10 hints/insights, prevent duplicate hints/insights (maybe regarding other users too)
        if 'hint' in request.POST:
            hint_form = HintForm(request.POST)
            if hint_form.is_valid() and request.user.is_authenticated:
                new_hint = Hint(
                    text=hint_form.cleaned_data.get('hint'),
                    problem_id=index,
                    username=request.user.username
                )
                new_hint.save()
        elif 'insight' in request.POST:
            insight_form = InsightForm(request.POST)
            if insight_form.is_valid() and request.user.is_authenticated:
                new_insight = Insight(
                    text=insight_form.cleaned_data.get('insight'),
                    problem_id=index,
                    username=request.user.username
                )
                new_insight.save()
        return redirect(f'/problems/{index}')
    
    problem = Problem.objects.get(id=index)
    clustered_hints = []
    hint_clusters = HintCluster.objects.filter(problem_id=index, first=True)[0:10]
    for cluster in hint_clusters:
        hints = Hint.objects.filter(id=cluster.hint_id)
        if hints.count() > 0:
            clustered_hints.append(hints.first())
    
    context = {
        'insight_form': insight_form,
        'hint_form': hint_form,
        'problem': problem,
        'clustered_hints': clustered_hints
    }
    if request.user.is_authenticated:
        user_hints = Hint.objects.filter(problem_id=index, username=request.user.username)
        user_insights = Insight.objects.filter(problem_id=index, username=request.user.username)
        context['user_hints'] = user_hints
        context['user_insights'] = user_insights
    return render(request, 'problems/problem.html', context)
