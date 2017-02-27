from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login

from forms import LoginForm, ResetPasswordForm
from captcha.client import request


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
  
@login_required
def admin_logout_view(request):
    logout(request)
    return redirect('/admin/login')

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


@login_required
def reset_password_view(request):
    form = ResetPasswordForm(request.POST or None, user=request.user)
    confirms = []
    if request.method == "POST":
        if form.is_valid():
            password_new = form.cleaned_data["new_password"]
            request.user.set_password(password_new)
            request.user.save()
            user = authenticate(username=request.user.username,
                                password=password_new)
            login(request, user)
            confirms.append("Parola a fost schimbata")
    print form.errors
    return render(request, "authentication/password_form.html", {
        "form": form,
        "confirms": confirms
    })
