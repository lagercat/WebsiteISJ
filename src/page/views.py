from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render

from models import Article, Category, SimplePage, Subcategory


def category(request, name):
    category_name = get_object_or_404(Category, title=name)
    subcat = Subcategory.objects.all().filter(category=category_name)
    simple_page = SimplePage.objects.all().filter(category=category_name)
    return render(request, 'page/category.html',
                  {
                      'name': category_name,
                      'subcategories': subcat,
                      'simple_pages': simple_page,
                  })


def category_all(request):
    categories = Category.objects.all()
    return render(request, 'page/category_all.html',
                  {
                      'categories_all':categories,
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
    subcat = get_object_or_404(Subcategory, name=name)
    articles = Article.objects.all().filter(subcategory=subcat)
    paginator = Paginator(articles, 4)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
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
