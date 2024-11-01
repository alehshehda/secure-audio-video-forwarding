from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistationForm

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'dashboard': 'dashboard'})


def user_registration(request):
    if request.method == 'POST':
        user_form = UserRegistationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistationForm()
    return render(request, 'account/register.html', {'user_form':user_form})
            
        
