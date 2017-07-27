# Copyright 2017 Adrian-Ioan Garovat, Emanuel Covaci, Sebastian-Valeriu Males
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
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
