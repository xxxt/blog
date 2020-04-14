import re

import markdown
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic import ListView
from markdown.extensions.toc import TocExtension
# 分页插件pure_pagination
# from pure_pagination import PaginationMixin

# Create your views here.
from blog.models import Blog, Tag, Category

from django.db.models.aggregates import Count

md = markdown.Markdown(extensions=[
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    # 'markdown.extensions.toc',
    TocExtension(slugify=slugify),
])

# 分页插件pure_pagination
# class IndexView(PaginationMixin, ListView):


class IndexBaseView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'texts'
    paginate_by = 4
    model = Blog


class IndexView(IndexBaseView):
    def get_queryset(self):
        texts = Blog.objects.all()
        for text in texts:
            text.abstract = md.convert(text.abstract)
        return texts


def detail(request, pk):
    article = get_object_or_404(Blog, pk=pk)

    article.body = md.convert(article.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    article.toc = m.group(1) if m is not None else ''
    # article.toc = md.toc
    article.increase_visiting()

    return render(request, 'blog/detail.html', context={'article': article})


def details(request, pk):
    article = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/test.html', context={'article': article})


def archives(request):
    context = {'date_list': Blog.objects.dates('created_time', 'month', order='DESC')}

    return render(request, 'blog/archive.html', context)


class ArchivesView(IndexBaseView):
    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        texts = Blog.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
        return texts


def categories(request):
    context = {'category_list': Category.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt=0), }
    return render(request, 'blog/categories.html', context=context)


class CategoriesView(IndexBaseView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs['pk'])
        texts = Blog.objects.filter(category=cate).order_by('-created_time')
        return texts


def tags(request):
    context = {'tag_list': Tag.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt=0)}
    return render(request, 'blog/tags.html', context=context)


class TagsView(IndexBaseView):
    def get_queryset(self):
        if self.kwargs:
            tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
            texts = Blog.objects.filter(tags=tag).order_by('-created_time')
            return texts
        else:
            self.template_name = 'blog/tags.html'
            self.context_object_name = 'context'
            context = {'tag_list': Tag.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt=0)}
            return context



