from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login

from forms import LoginForm


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    if request.user.is_authenticated():
        return redirect('/')
    form = LoginForm(request.POST)
    errors = []
    if request.method == "POST":
        if form.is_valid():
            user = authenticate(user=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('/')
            else:
                errors.append("Nume de utilizator sau parola invalida")
    return render(request, 'authentication/login.html', {
        'errors': errors,
        'form': form
    })
