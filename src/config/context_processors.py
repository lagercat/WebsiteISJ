
from subject.models import Subject
from page.models import Category, Subcategory,SimplePage


def template_context(request):
    subjects = Subject.objects.all()
    category = Category.objects.all()
    header = {
        value.title: list(
            Subcategory.objects.all().filter(category=value).order_by(
                "name").values("name", ))[:7] for value in category
        }
    simple_page = {
        value.title: list(
            SimplePage.objects.all().filter(category=value).order_by(
                "name").values("name", ))[:7] for value in category
        }
    print header.items()
    return {

        'header': header.items(),
        'simple_page': simple_page.items(),
        'subjects': subjects,
     }