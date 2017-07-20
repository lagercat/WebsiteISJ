from page.models import Category
from subject.models import Subject


def template_context(request):

    return {
        'categories': Category.objects.all()[:7],
        'categories_number':Category.objects.all().count(),
        'left_subjects': Subject.objects.all()
    }
