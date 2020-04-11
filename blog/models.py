import markdown
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from mdeditor.fields import MDTextField


class Category(models.Model):
    """分类"""

    name = models.CharField(max_length=128, verbose_name='分类')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_category'
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """标签"""

    name = models.CharField(max_length=128, verbose_name='标签')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_tag'
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Blog(models.Model):

    title = models.CharField(max_length=1024, verbose_name='标题')
    author = models.ForeignKey(User, default='xx', verbose_name='作者', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='blog_img', null=True, blank=True, verbose_name='博客图片')
    body = MDTextField(verbose_name='正文')
    abstract = models.TextField(max_length=256, null=True, blank=True, verbose_name='摘要')
    visiting = models.PositiveIntegerField(default=0, verbose_name='访问量')
    category = models.ManyToManyField(Category, verbose_name='博客分类')
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modifyed_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_blog'
        ordering = ['-created_time']
        verbose_name = '博客'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse("blog:blog_detail", kwargs={"blog_id": self.id})

    def increase_visiting(self):
        self.visiting += 1
        self.save(update_fields=['visiting'])

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        self.abstract = strip_tags(md.convert(self.body))[:256]
        super().save(*args, **kwargs)


class User(models.Model):

    no = models.AutoField(primary_key=True, verbose_name='编号')
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='用户密码')
    email = models.EmailField(max_length=255, default='', blank=True, verbose_name='邮箱')

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
