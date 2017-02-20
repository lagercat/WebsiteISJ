from subject.models import Subject
from page.models import Category, Subcategory, SimplePage


def template_context(request):

    return {
        'categories': Category.objects.all(),
    }
