
from subject.models import Subject
from page.models import Category, Subcategory


def template_context(request):
    subjects = Subject.objects.all()
    category = Category.objects.all()
    header = {
        value.title: list(
            Subcategory.objects.all().filter(category=value).order_by(
                "name").values("name", ))[:7] for value in category
        }
    return {

        'header': header.items(),
        'subjects': subjects,
     }