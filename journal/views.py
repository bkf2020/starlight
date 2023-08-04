import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JournalProblem, JournalConfig
from .forms import ProblemStatusForm
from problems.models import Insight, Problem

# Create your views here.
@login_required
def journal(request):
    if request.method == 'POST':
        problem_status_form = ProblemStatusForm(request.POST)
        if problem_status_form.is_valid() and request.user.is_authenticated:
            problem_id = problem_status_form.cleaned_data.get('problem_id')
            status = problem_status_form.cleaned_data.get('status')
            curr_journal_problem = JournalProblem.objects.filter(username=request.user.username, problem_id=problem_id)
            # TODO: handle no curr_journal_problem exisiting
            if curr_journal_problem.count() > 0:
                curr_journal_problem = curr_journal_problem.first()
                curr_journal_problem.status = status
                curr_journal_problem.save()
        return redirect('/journal/')
    
    today = datetime.date.today()
    if JournalConfig.objects.filter(username=request.user.username).count() == 0:
        journal_config = JournalConfig(username=request.user.username)
        journal_config.save()
    else:
        journal_config = JournalConfig.objects.filter(username=request.user.username).first()
    if request.GET.get('type') == "" or request.GET.get('type') == None:
        return redirect(f'/journal/?type={journal_config.type_filter}')
    if request.GET.get('type') == "entire":
        journal_config.type_filter = "entire"
        journal_config.save()
        user_journal_problems = JournalProblem.objects.filter(username=request.user.username).order_by("-time_created")
    elif request.GET.get('type') == "week":
        week_filter = request.GET.get('week')
        year_filter = request.GET.get('year')
        if request.GET.get('week') == None or request.GET.get('week') == "":
            week_filter = today.isocalendar().week
            if journal_config.type_filter == "week":
                week_filter = journal_config.desired_week
        if request.GET.get('year') == None or request.GET.get('year') == "":
            year_filter = today.year
            if journal_config.type_filter == "week":
                year_filter = journal_config.desired_year
            return redirect(f'/journal/?type=week&week={week_filter}&year={year_filter}')
        journal_config.type_filter = "week"
        journal_config.desired_week = week_filter
        journal_config.desired_year = year_filter
        journal_config.save()
        user_journal_problems = JournalProblem.objects.filter(username=request.user.username, time_created__week=week_filter, time_created__iso_year=year_filter).order_by("-time_created")
    elif request.GET.get('type') == "month":
        month_filter = request.GET.get('month')
        year_filter = request.GET.get('year')
        if request.GET.get('month') == None or request.GET.get('month') == "":
            month_filter = today.month
            if journal_config.type_filter == "month":
                month_filter = journal_config.desired_month
        if request.GET.get('year') == None or request.GET.get('year') == "":
            year_filter = today.year
            if journal_config.type_filter == "month":
                year_filter = journal_config.desired_year
            return redirect(f'/journal/?type=month&month={month_filter}&year={year_filter}')
        journal_config.type_filter = "month"
        journal_config.desired_month = month_filter
        journal_config.desired_year = year_filter
        journal_config.save()
        user_journal_problems = JournalProblem.objects.filter(username=request.user.username, time_created__month=month_filter, time_created__year=year_filter).order_by("-time_created")
    elif request.GET.get('type') == "year":
        year_filter = request.GET.get('year')
        if request.GET.get('year') == None or request.GET.get('year') == "":
            year_filter = today.year
            if journal_config.type_filter == "year":
                year_filter = journal_config.desired_year
            return redirect(f'/journal/?type=year&year={year_filter}')
        journal_config.type_filter = "year"
        journal_config.save()
        user_journal_problems = JournalProblem.objects.filter(username=request.user.username, time_created__year=year_filter).order_by("-time_created")

    idx = 0
    for journal_problem in user_journal_problems:
        journal_problem.insights = Insight.objects.filter(username=request.user.username, problem_id=journal_problem.problem.id)
        journal_problem.form = ProblemStatusForm(auto_id=str(idx) + '_%s', initial={'problem_id': journal_problem.problem.id, 'status': journal_problem.status})
        idx += 1
    context = {
        'user_journal_problems': user_journal_problems
    }
    return render(request, 'journal/journal.html', context)


@login_required
def create(request, index):
    desired_problem = Problem.objects.get(id=index)
    if JournalProblem.objects.filter(username=request.user.username, problem=desired_problem).count() == 0:
        new_journal_problem = JournalProblem(username=request.user.username, problem=desired_problem)
        new_journal_problem.save()
        messages.success(request, f"Problem {desired_problem.name} successfully added to journal")
    else:
        messages.info(request, f"Problem {desired_problem.name} already in the journal")
    if request.GET.get('next') == None or request.GET.get('next') == "":
        return redirect('/problems/')
    return redirect(request.GET.get('next'))