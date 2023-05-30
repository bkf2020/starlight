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
    else:
        if search_type == 'group':
            insight_cluster_id = request.GET.get('cluster')
            insight_problem_id = request.GET.get('problem')
            insight_cluster = InsightCluster.objects.filter(cluster_id=insight_cluster_id, problem_id=insight_problem_id)
            firstProblem = Problem.objects.filter(id=insight_problem_id)
            if firstProblem.count() > 0:
                firstProblem = firstProblem.first()
            else:
                firstProblem = Problem(name="N/A", url="#")
        else:
            insight_problem_id = request.GET.get('problem')
            insight_cluster = InsightCluster.objects.filter(problem_id=insight_problem_id)
            firstProblem = Problem.objects.filter(id=insight_problem_id)
            if firstProblem.count() > 0:
                firstProblem = firstProblem.first()
            else:
                firstProblem = Problem(name="N/A", url="#")

        problems = []
        id_problem = {}
        seen_cluster_id_overall = {}
        for insight_info in insight_cluster:
            cluster_id_overall = OverallInsightCluster.objects.filter(insight=insight_info.insight).first().cluster_id_overall
            overall_cluster = OverallInsightCluster.objects.filter(cluster_id_overall=cluster_id_overall)
            if cluster_id_overall in seen_cluster_id_overall:
                continue
            seen_cluster_id_overall[cluster_id_overall] = True

            seen_problem = {}
            for info in overall_cluster:
                problem = Problem.objects.filter(id=info.problem_id)
                if info.problem_id in seen_problem:
                    continue
                seen_problem[info.problem_id] = True

                if problem.count() > 0:
                    if info.problem_id in id_problem:
                        id_problem[info.problem_id].insights_matched.append(overall_cluster.filter(problem_id=info.problem_id))
                    else:
                        add_problem = problem.first()
                        add_problem.insights_matched = [overall_cluster.filter(problem_id=info.problem_id)]
                        id_problem[info.problem_id] = add_problem
        for problem_id in id_problem:
            problems.append(id_problem[problem_id])
        context = {
            'problems': problems,
            'firstProblem': firstProblem,
            'firstInsight': insight_cluster[0].insight
        }
        return render(request, 'problems/problems_similar_insights.html', context)

def shared_insights(request):
    search_type = request.GET.get('type')
    if search_type == "individual":
        insight_id = request.GET.get('insight')
        insight = Insight.objects.filter(id=insight_id).first()
        other_problem_id = request.GET.get('otherProblem')
        otherProblem = Problem.objects.filter(id=other_problem_id).first()
        firstProblem = Problem.objects.filter(id=insight.problem_id)
        if firstProblem.count() > 0:
            firstProblem = firstProblem.first()
        else:
            firstProblem = Problem(name="N/A", url="#")
        cluster_id_overall = OverallInsightCluster.objects.filter(insight=insight).first().cluster_id_overall
        shared_insights = OverallInsightCluster.objects.filter(cluster_id_overall=cluster_id_overall, problem_id=other_problem_id)
        context = {
            'insight': insight,
            'shared_insights': shared_insights,
            'firstProblem': firstProblem,
            'otherProblem': otherProblem
        }
        return render(request, 'problems/shared_insights.html', context)
    else:
        if search_type == 'group':
            insight_cluster_id = request.GET.get('cluster')
            insight_problem_id = request.GET.get('insightProblem')
            insight_cluster = InsightCluster.objects.filter(cluster_id=insight_cluster_id, problem_id=insight_problem_id)
            firstProblem = Problem.objects.filter(id=insight_problem_id)
            if firstProblem.count() > 0:
                firstProblem = firstProblem.first()
            else:
                firstProblem = Problem(name="N/A", url="#")
            other_problem_id = request.GET.get('otherProblem')
            otherProblem = Problem.objects.filter(id=other_problem_id).first()
        else:
            first_problem_id = request.GET.get('firstProblem')
            firstProblem = Problem.objects.filter(id=first_problem_id)
            if firstProblem.count() > 0:
                firstProblem = firstProblem.first()
            else:
                firstProblem = Problem(name="N/A", url="#")
            insight_cluster = InsightCluster.objects.filter(problem_id=first_problem_id)
            other_problem_id = request.GET.get('otherProblem')
            otherProblem = Problem.objects.filter(id=other_problem_id).first()
        
        seen_cluster_id_overall = {}
        shared_insights = []
        for insight_info in insight_cluster:
            cluster_id_overall = OverallInsightCluster.objects.filter(insight=insight_info.insight).first().cluster_id_overall
            overall_cluster = OverallInsightCluster.objects.filter(cluster_id_overall=cluster_id_overall)
            if cluster_id_overall in seen_cluster_id_overall:
                continue
            seen_cluster_id_overall[cluster_id_overall] = True
            shared_insights.append(overall_cluster.filter(problem_id=other_problem_id))
        context = {
            'shared_insights': shared_insights,
            'firstProblem': firstProblem,
            'firstInsight': insight_cluster[0].insight,
            'otherProblem': otherProblem
        }
        return render(request, 'problems/shared_insights.html', context)