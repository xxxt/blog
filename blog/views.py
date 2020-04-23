import re
import json
import markdown
import requests
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import ListView
from django.views.generic.base import View
from markdown.extensions.toc import TocExtension
from blog.forms import RegisterForm, LoginForm, TEL_PATTERN
from blog.utils import generate_captcha_code, generate_mobile_code
from blog.captcha import Captcha
# 分页插件pure_pagination
# from pure_pagination import PaginationMixin

# Create your views here.
from blog.models import Blog, Tag, Category, User
from comment.models import Comment
from blog.forms import BlogPostForm, MDEditorForm

from django.db.models.aggregates import Count

md = markdown.Markdown(extensions=[
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    # 'markdown.extensions.toc',
    TocExtension(slugify=slugify),
])


# 分页插件pure_pagination
# class IndexView(PaginationMixin, ListView):


class IndexBaseView(ListView):  # 列表展示类，包含分页功能
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
    comments = Comment.objects.filter(article=pk).order_by('-created')
    article.increase_visiting()
    return render(request, 'blog/test.html', context={'article': article, 'comments': comments})


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


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    post_list = Blog.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'texts': post_list, 'q': q})


class SearchView(IndexBaseView):
    # def get_context_data(self, **kwargs):
    #     q = self.request.GET.get('q')
    #     context = super(SearchView, self).get_context_data(**kwargs)
    #     context['q'] = q
    #     return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        if not q:
            error_msg = "请输入搜索关键词"
            messages.add_message(self.request, messages.ERROR, error_msg, extra_tags='danger')
            return redirect('blog:index')

        texts = Blog.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))

        return texts


def article_create(request):
    if request.session['userid'] == 2:
        if request.method == "POST":
            article_post_form = BlogPostForm(data=request.POST)
            content_form = MDEditorForm(request.POST)
            if article_post_form.is_valid():
                new_article = article_post_form.save(commit=False)
                new_article.author = User.objects.get(no=request.session['userid'])
                # if request.POST['category'] != 'none':
                    # new_article.colum = Category.objects.get(id=request.POST['category'])

                # if request.POST['tag'] != 'none':
                #     new_article.tags = Category.objects.get(id=request.POST['tag'])
                # new_article.category.add(Category.objects.get[])
                # new_article.tags = '网络'
                new_article.save()
                new_article.category.add(Category.objects.get(id=request.POST['category']))
                new_article.tags.add(Tag.objects.get(id=request.POST['tag']))
                return redirect('blog:index')
            else:
                return HttpResponse("表单内容有误，请重新填写。")
        else:
            article_post_form = BlogPostForm()
            categories = Category.objects.all()
            tags = Tag.objects.all()
            context = {'article_post_form': article_post_form, 'categories': categories, 'tags': tags}
            return render(request, 'blog/create.html', context)
    else:
        return render(request, 'blog/create.html', {'error': '您无权发表文章'})


def get_mobile_code(request):
    """获得手机验证码"""
    tel = request.GET.get('tel')
    if TEL_PATTERN.fullmatch(tel):
        code = generate_mobile_code()
        request.session['mobile_code'] = code
        resp = requests.post(
            url='http://sms-api.luosimao.com/v1/send.json',
            auth=('api', 'key-6d2417156fefbd9c0e78fae069a34580'),
            data={
                'mobile': tel,
                'message': f'您的短信验证码是{code}，打死也不能告诉别人。【Python小课】',
            },
            timeout=3,
            verify=False
        )
        if json.loads(resp.text)['error'] == 0:
            code, hint = 20001, '短信验证码发送成功'
        else:
            code, hint = 20002, '短信验证码发送失败，请稍后重试'
    else:
        code, hint = 20003, '请输入有效的手机号码'
    return JsonResponse({'code': code, 'hint': hint})


def register(request):
    """用户注册"""
    hint = ''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            code_from_session = '123456'  # request.session.get('mobile_code')
            code_from_user = form.cleaned_data['code']
            if code_from_session == code_from_user:
                form.save()
                hint = '注册成功，请登录!'
                return render(request, 'blog/login.html', {'hint': hint})
            else:
                hint = '请输入正确的手机验证码'
        else:
            hint = '请输入有效的注册信息'
    return render(request, 'blog/register.html', {'hint': hint})


def login(request):
    """用户登录"""
    hint = ''
    backurl = request.GET.get('backurl', '/')
    if request.method == 'POST':
        backurl = request.POST['backurl']
        form = LoginForm(request.POST)
        if form.is_valid():
            code_from_session = request.session.get('captcha_code')
            code_from_user = form.cleaned_data['code']
            if code_from_session.lower() == code_from_user.lower():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = User.objects.filter(
                    username=username, password=password).first()
                if user:
                    request.session['userid'] = user.no
                    request.session['username'] = user.username
                    return redirect(backurl)
                else:
                    hint = '用户名或密码错误'
            else:
                hint = '请输入正确的验证码'
        else:
            hint = '请输入有效的登录信息'
    return render(request, 'blog/login.html', {'hint': hint, 'backurl': backurl})


def get_captcha(request):
    """生成图片验证码"""
    code = generate_captcha_code()
    request.session['captcha_code'] = code
    image_data = Captcha.instance().generate(code, fmt='PNG')
    return HttpResponse(image_data, content_type='image/png')


def logout(request):
    """用户注销"""
    request.session.flush()
    return redirect('blog:index')


class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = Blog.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')


def about(request):
    context = {'name': 'yjh'}
    return render(request, 'blog/about.html', context)

# TODO
#  add categroy in UI
#  test
#  cache
