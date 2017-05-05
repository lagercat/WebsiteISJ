from page.models import Category


def template_context(request):

    return {
        'categories': Category.objects.all(),
    }
