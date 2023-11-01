from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ImportStatus

@login_required
def import_view(request):
    possible_status = ImportStatus.objects.filter(username=request.user.username)
    if possible_status.count() > 0:
        current_status = possible_status.first()
    else:
        current_status = ImportStatus(status="NP")
    context = {
        'current_status': current_status
    }
    return render(request, 'import/import.html', context)