from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, 'about/about.html')
def privacy(request):
    return render(request, 'about/privacy.html')
def rules(request):
    return render(request, 'about/rules.html')
