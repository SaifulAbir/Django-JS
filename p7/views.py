from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='professional/sign-in/')
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
