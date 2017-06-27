from page.models import Category
from subject.models import Subject


def template_context(request):
    return {
        'categories': Category.objects.all(),
        'left_subjects': Subject.objects.all()
    }
