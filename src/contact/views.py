from django.shortcuts import render
from .forms import CreateContactForm


def contact(request):
    confirm = []
    form = CreateContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm.append(
                'Your message has been successfully sent!\nThank you!')
            form = CreateContactForm(None)
    return render(request, 'contact/contact.html',
                  {'form': form,
                   'confirm': confirm}
                  )
