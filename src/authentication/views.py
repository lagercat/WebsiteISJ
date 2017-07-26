from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from forms import LoginForm, ResetPasswordForm


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def admin_logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    if request.user.is_authenticated():
        return redirect('/')
    form = LoginForm(request.POST)
    errors = []
    if request.method == "POST":
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/admin')
            else:
                errors.append("Email sau parola invalida / Cont dezactivat")
    return render(request, 'authentication/login.html', {
        'errors': errors,
        'form': form
    })
