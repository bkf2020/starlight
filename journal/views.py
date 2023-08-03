from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JournalProblem
from .forms import ProblemStatusForm
from problems.models import Insight, Problem

# Create your views here.
@login_required
def journal(request):
    user_journal_problems = JournalProblem.objects.filter(username=request.user.username)
    idx = 0
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