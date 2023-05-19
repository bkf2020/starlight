from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from .models import Problem, Hint, Insight, HintCluster, InsightCluster, OverallInsightCluster
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
    hint_clusters = HintCluster.objects.filter(problem_id=index, first=True)[0:10]
    insight_clusters = InsightCluster.objects.filter(problem_id=index, first=True)[0:10]
    
    context = {
        'insight_form': insight_form,
        'hint_form': hint_form,
        'problem': problem,
        'hint_clusters': hint_clusters,
        'insight_clusters': insight_clusters
    }
    if request.user.is_authenticated:
        user_hints = Hint.objects.filter(problem_id=index, username=request.user.username)
        user_insights = Insight.objects.filter(problem_id=index, username=request.user.username)
        context['user_hints'] = user_hints
        context['user_insights'] = user_insights
    return render(request, 'problems/problem.html', context)

# TODO: add pagination
def view_cluster(request):
    cluster_id = request.GET.get('cluster')
    problem_id = request.GET.get('problem')
    search_hint = request.GET.get('type') == "hint"
    if search_hint:
        cluster = HintCluster.objects.filter(cluster_id=cluster_id, problem_id=problem_id)
        hints = []
        for hint_info in cluster:
            hints.append(hint_info.hint)
        context = {
            'hints': hints
        }
        return render(request, 'problems/view_cluster.html', context)
    else:
        cluster = InsightCluster.objects.filter(cluster_id=cluster_id, problem_id=problem_id)
        insights = []
        for insight_info in cluster:
            insights.append(insight_info.insight)
        context = {
            'insights': insights
        }
        return render(request, 'problems/view_cluster.html', context)

def problems_similar_insights(request):
    search_type = request.GET.get('type')
    if search_type == "individual":
        insight_id = request.GET.get('insight')
        insight = Insight.objects.filter(id=insight_id).first()
        firstProblem = Problem.objects.filter(id=insight.problem_id)
        if firstProblem.count() > 0:
            firstProblem = firstProblem.first()
        else:
            firstProblem = Problem(name="N/A", url="#")
        cluster_id_overall = OverallInsightCluster.objects.filter(insight=insight).first().cluster_id_overall
        cluster = OverallInsightCluster.objects.filter(cluster_id_overall=cluster_id_overall)
        problems = []
        seen = {}
        for info in cluster:
            if info.problem_id in seen:
                continue
            seen[info.problem_id] = True
            problem = Problem.objects.filter(id=info.problem_id)
            if problem.count() > 0:
                add_problem = problem.first()
                add_problem.insights_matched = cluster.filter(problem_id=add_problem.id)
                problems.append(add_problem)
        context = {
            'insight': insight,
            'cluster': cluster,
            'problems': problems,
            'firstProblem': firstProblem
        }
        return render(request, 'problems/problems_similar_insights.html', context)