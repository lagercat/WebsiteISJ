from django.shortcuts import render, get_object_or_404
from models import Category,Subcategory,Article


# Create your views here.

def category(request, name):
    category_name = get_object_or_404(Category, title=name)
    subcategory = Subcategory.objects.all().filter(category=category_name)
    print subcategory
    return render(request, 'page/category.html',
                  {
                      'name': category_name,
                      'subcategories':subcategory,
                  })