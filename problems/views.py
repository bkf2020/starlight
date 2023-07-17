from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponseNotFound
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
    def get_success_url(self):
        return f"/problems/{self.get_object().problem_id}?type=hint"
    def test_func(self):
        return self.request.user.username == self.get_object().username

class InsightUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Insight
    fields = ['text']
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return f"/problems/{self.get_object().problem_id}?type=insight"
    def test_func(self):
        return self.request.user.username == self.get_object().username

class HintDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Hint
    fields = ['text']
    template_name_suffix = '_confirm_delete'
    def get_success_url(self):
        return f"/problems/{self.get_object().problem_id}?type=hint"
    def test_func(self):
        return self.request.user.username == self.get_object().username

class InsightDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Insight
    fields = ['text']
    template_name_suffix = '_confirm_delete'
    def get_success_url(self):
        return f"/problems/{self.get_object().problem_id}?type=insight"
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
            return redirect(f'/problems/{index}?type=hint#id_hint')
        elif 'insight' in request.POST:
            insight_form = InsightForm(request.POST)
            if insight_form.is_valid() and request.user.is_authenticated:
                new_insight = Insight(
                    text=insight_form.cleaned_data.get('insight'),
                    problem_id=index,
                    username=request.user.username
                )
                new_insight.save()
            return redirect(f'/problems/{index}?type=insight#id_insight')
        return redirect(f'/problems/{index}')
    
    problem = Problem.objects.get(id=index)
    
    context = {
        'insight_form': insight_form,
        'hint_form': hint_form,
        'problem': problem
    }
    if request.user.is_authenticated:
        user_hints = Hint.objects.filter(problem_id=index, username=request.user.username).order_by("id")
        user_insights = Insight.objects.filter(problem_id=index, username=request.user.username).order_by("id")
        context['user_hints'] = user_hints
        context['user_insights'] = user_insights
    return render(request, 'problems/problem.html', context)

def view_all_hints_insights(request):
    search_type = request.GET.get('type')
    problem_id = request.GET.get('problem')
    problem = Problem.objects.filter(id=problem_id).first()
    if search_type == "hint":
        hints_insights = Hint.objects.filter(problem_id=problem_id).order_by('id')
    else:
        hints_insights = Insight.objects.filter(problem_id=problem_id).order_by('id')
    paginator = Paginator(hints_insights, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'problem': problem
    }
    return render(request, 'problems/view_all_hints_insights.html', context)

def view_cluster(request):
    cluster_id = request.GET.get('cluster')
    problem_id = request.GET.get('problem')
    search_hint = request.GET.get('type') == "hint"
    use_json = request.GET.get('json') == "true"
    if search_hint:
        cluster = HintCluster.objects.filter(cluster_id=cluster_id, problem_id=problem_id).order_by('id')
        hints = []
        for hint_info in cluster:
            if use_json:
                hints.append(model_to_dict(hint_info.hint))
            else:
                hints.append(hint_info.hint)
        paginator = Paginator(hints, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if use_json:
            new_page_obj = {}
            new_page_obj["hints"] = []
            for hint in page_obj:
                new_page_obj["hints"].append(hint)
            new_page_obj["num_pages"] = page_obj.paginator.num_pages
            new_page_obj["has_previous"] = page_obj.has_previous()
            new_page_obj["has_next"] = page_obj.has_next()
            new_page_obj["number"] = page_obj.number
            context = {
                'new_page_obj': new_page_obj
            }
            return JsonResponse(context)
        else:
            context = {
                'page_obj': page_obj
            }
        return render(request, 'problems/view_cluster.html', context)
    else:
        cluster = InsightCluster.objects.filter(cluster_id=cluster_id, problem_id=problem_id).order_by('id')
        insights = []
        for insight_info in cluster:
            if use_json:
                insights.append(model_to_dict(insight_info.insight))
            else:
                insights.append(insight_info.insight)
        paginator = Paginator(insights, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if use_json:
            new_page_obj = {}
            new_page_obj["insights"] = []
            for insight in page_obj:
                new_page_obj["insights"].append(insight)
            new_page_obj["num_pages"] = page_obj.paginator.num_pages
            new_page_obj["has_previous"] = page_obj.has_previous()
            new_page_obj["has_next"] = page_obj.has_next()
            new_page_obj["number"] = page_obj.number
            context = {
                'new_page_obj': new_page_obj
            }
            return JsonResponse(context)
        else:
            context = {
                'page_obj': page_obj
            }
        return render(request, 'problems/view_cluster.html', context)

def view_all_summary(request):
    problem_id = request.GET.get('problem')
    problem = Problem.objects.filter(id=problem_id).first()
    search_hint = request.GET.get('type') == "hint"
    if search_hint:
        hints_insights = []
        for pos, hint in enumerate(HintCluster.objects.filter(problem_id=problem_id, first=True).order_by('cluster_id'), start=1):
            hint.pos = pos
            hint.cluster_size = HintCluster.objects.filter(problem_id=problem_id).count()
            hints_insights.append(hint)
    else:
        hints_insights = []
        for cluster in InsightCluster.objects.filter(problem_id=problem_id, first=True).order_by('cluster_id'):
            cluster.cluster_size = InsightCluster.objects.filter(problem_id=problem_id).count()
            hints_insights.append(cluster)
    hint_insights = sorted(hints_insights, key=lambda hint_insight: (hint_insight.cluster_size, hint_insight.id), reverse=True)
    paginator = Paginator(hints_insights, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'problem': problem
    }
    return render(request, 'problems/view_all_summary.html', context)

def problems_similar_insights(request):
    search_type = request.GET.get('type')
    json = request.GET.get('json') == "true"
    if search_type == "individual":
        insight_id = request.GET.get('insight')
        insight = Insight.objects.filter(id=insight_id).first()
        try:
            firstProblem = Problem.objects.filter(id=insight.problem_id)
        except:
            return HttpResponseNotFound("404 error with individual insight specified/insight not specified/insight not found")
        if firstProblem.count() > 0:
            firstProblem = firstProblem.first()
        else:
            return HttpResponseNotFound("404 problem not found")
        try:
            cluster_id_overall = OverallInsightCluster.objects.filter(insight=insight).first().cluster_id_overall
        except AttributeError:
            return HttpResponseNotFound("404 error with insight specified/the system has not considered problems similar to this insight yet")
        cluster = OverallInsightCluster.objects.filter(cluster_id_overall=cluster_id_overall)
        problems = []
        seen = {}
        for info in cluster:
            if info.problem_id in seen or info.problem_id == firstProblem.id:
                continue
            seen[info.problem_id] = True
            problem = Problem.objects.filter(id=info.problem_id)
            if problem.count() > 0:
                add_problem = problem.first()
                insights_from_problem = cluster.filter(problem_id=add_problem.id)
                add_problem.insights_matched = []
                for insight_info in insights_from_problem:
                    if len(add_problem.insights_matched) == 10:
                        break
                    add_problem.insights_matched.append(insight_info)
                add_problem.insights_matched_size = insights_from_problem.count()
                problems.append(add_problem)
        problems = sorted(problems, key=lambda problem: (problem.insights_matched_size, problem.id), reverse=True)
        paginator = Paginator(problems, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'insight': insight,
            'cluster': cluster,
            'page_obj': page_obj,
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
                return HttpResponseNotFound("404 problem not found")
        else:
            insight_problem_id = request.GET.get('problem')
            insight_cluster = InsightCluster.objects.filter(problem_id=insight_problem_id)
            firstProblem = Problem.objects.filter(id=insight_problem_id)
            if firstProblem.count() > 0:
                firstProblem = firstProblem.first()
            else:
                return HttpResponseNotFound("404 problem not found")

        problems = []
        id_problem = {}
        seen_cluster_id_overall = {}
        if insight_cluster.count() == 0:
            context = {
                "none_in_cluster": True
            }
            if json: return JsonResponse(context)
            return render(request, 'problems/problems_similar_insights.html', context)
        for insight_info in insight_cluster:
            try:
                cluster_id_overall = OverallInsightCluster.objects.filter(insight=insight_info.insight).first().cluster_id_overall
            except:
                if json:
                    context = {'not_all_similar': True}
                    return JsonResponse(context)
                return HttpResponseNotFound("please try again later... not all similar problems have been considered")
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
                        insights_from_problem = overall_cluster.filter(problem_id=info.problem_id).order_by('id')
                        for insight_info in insights_from_problem:
                            if len(id_problem[info.problem_id].insights_matched) == 10:
                                break
                            if json:
                                id_problem[info.problem_id].insights_matched.append(model_to_dict(insight_info.insight))
                            else:
                                id_problem[info.problem_id].insights_matched.append(insight_info)
                        id_problem[info.problem_id].insights_matched_size += insights_from_problem.count()
                    else:
                        add_problem = problem.first()
                        insights_from_problem = overall_cluster.filter(problem_id=info.problem_id).order_by('id')
                        add_problem.insights_matched = []
                        for insight_info in insights_from_problem:
                            if len(add_problem.insights_matched) == 10:
                                break
                            if json:
                                add_problem.insights_matched.append(model_to_dict(insight_info.insight))
                            else:
                                add_problem.insights_matched.append(insight_info)
                        id_problem[info.problem_id] = add_problem
                        id_problem[info.problem_id].insights_matched_size = insights_from_problem.count()
        id_problem = dict(sorted(id_problem.items(), key=lambda problem: (problem[1].insights_matched_size, problem[0]), reverse=True))
        for problem_id in id_problem:
            if str(problem_id) == insight_problem_id:
                continue
            if json:
                problem_dict = model_to_dict(id_problem[problem_id])
                problem_dict["insights_matched"] = id_problem[problem_id].insights_matched
                problems.append(problem_dict)
            else:
                problems.append(id_problem[problem_id])
        paginator = Paginator(problems, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if json:
            new_page_obj = {}
            new_page_obj["problems"] = []
            for problem in page_obj:
                new_page_obj["problems"].append(problem)
            new_page_obj["num_pages"] = page_obj.paginator.num_pages
            new_page_obj["has_previous"] = page_obj.has_previous()
            new_page_obj["has_next"] = page_obj.has_next()
            new_page_obj["number"] = page_obj.number
            context = {
                'new_page_obj': new_page_obj,
                'firstProblem': model_to_dict(firstProblem),
                'firstInsight': model_to_dict(insight_cluster[0].insight)
            }
            return JsonResponse(context)
        else:
            context = {
                'page_obj': page_obj,
                'firstProblem': firstProblem,
                'firstInsight': insight_cluster[0].insight
            }
        return render(request, 'problems/problems_similar_insights.html', context)

def shared_insights(request):
    search_type = request.GET.get('type')
    json = request.GET.get('json') == "true"
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
        shared_insights = OverallInsightCluster.objects.filter(cluster_id_overall=cluster_id_overall, problem_id=other_problem_id).order_by('id')
        paginator = Paginator(shared_insights, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'insight': insight,
            'page_obj': page_obj,
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
            for insight_info in overall_cluster.filter(problem_id=other_problem_id).order_by('id'):
                if json:
                    shared_insights.append(model_to_dict(insight_info.insight))
                else:
                    shared_insights.append(insight_info.insight)
        paginator = Paginator(shared_insights, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if json:
            new_page_obj = {}
            new_page_obj["shared_insights"] = []
            for insight in page_obj:
                new_page_obj["shared_insights"].append(insight)
            new_page_obj["num_pages"] = page_obj.paginator.num_pages
            new_page_obj["has_previous"] = page_obj.has_previous()
            new_page_obj["has_next"] = page_obj.has_next()
            new_page_obj["number"] = page_obj.number
            context = {
                'new_page_obj': new_page_obj,
                'firstProblem': model_to_dict(firstProblem),
                'firstInsight': model_to_dict(insight_cluster[0].insight),
            'otherProblem': model_to_dict(otherProblem)
            }
            return JsonResponse(context)
        context = {
            'page_obj': page_obj,
            'firstProblem': firstProblem,
            'firstInsight': insight_cluster[0].insight,
            'otherProblem': otherProblem
        }
        return render(request, 'problems/shared_insights.html', context)