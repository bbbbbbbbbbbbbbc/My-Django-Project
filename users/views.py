from django.shortcuts import render, redirect  
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm 
from django.http import Http404
def register(request): 
    """注册新用户。""" 
    if request.method == 'GET': 
        form = UserCreationForm()
    elif request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save() 
            login(request, new_user) 
            return redirect('learning_logs:index') 
    else:
        raise Http404("Wrong Request Method")
    context = {'form': form} 
    return render(request, 'registration/register.html', context)
