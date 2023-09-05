from django.shortcuts import render
from django.utils import timezone

# Create your views here.
def about(request):
    return render(request, 'about/about.html')
def privacy(request):
    return render(request, 'about/privacy.html')
def rules(request):
    return render(request, 'about/rules.html')
def challenge(request):
    curr_server_time = timezone.now().timestamp()
    return render(request, 'about/challenge.html', {'curr_server_time': curr_server_time})
