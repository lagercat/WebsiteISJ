from django.shortcuts import render, get_object_or_404
from models import Category, Subcategory, Article, SimplePage


# Create your views here.

def category(request, name):
    category_name = get_object_or_404(Category, title=name)
    subcategory = Subcategory.objects.all().filter(category=category_name)
    simple_page = SimplePage.objects.all().filter(category=category_name)
    print simple_page
    print subcategory
    return render(request, 'page/category.html',
                  {
                      'name': category_name,
                      'subcategories': subcategory,
                      'simple_pages':simple_page,
                  })


def subcategory_article(request, name, slug):
    article = list(
        Article.objects.values('name', 'text', 'subcategory', 'file', 'date',
                               'slug').filter(slug=slug,
                                              subcategory=name))
    return render(request, 'subject/subject_news.html', {

        'name': article[0].get('name'),
        'text': article[0].get('text'),
        'thumbnail': "/media/" + article[0].get('file'),

    })


def subcategory(request, name):
    subcategory = get_object_or_404(Subcategory, name=name)
    articles = Article.objects.all().filter(subcategory=subcategory)
    return render(request, 'page/subcategory.html',
                  {'name': name,
                   'articole': articles,
                   })


def article_post(request, name, slug):
    article = list(
        Article.objects.values('subcategory', 'name', 'text', 'file',
                               'date').filter(slug=slug))
    return render(request, 'page/article.html', {

        'name': article[0].get('name'),
        'text': article[0].get('text'),
        'date': article[0].get('date'),
        'thumbnail': "/media/" + article[0].get('file'),

    })


def simple_page_article(request, slug):
    article = list(
        SimplePage.objects.values('category', 'name', 'text', 'file',
                                  'date').filter(slug=slug))
    return render(request, 'page/article.html', {

        'name': article[0].get('name'),
        'text': article[0].get('text'),
        'date': article[0].get('date'),
        'thumbnail': "/media/" + article[0].get('file'),

    })
