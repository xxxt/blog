from django.contrib import admin

# Register your models here.

from blog import models
from blog.forms import UserForm
# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'visiting', 'created_time', 'modifyed_time')
    # ordering = ('visiting', )


class UserAdmin(admin.ModelAdmin):
    list_display = ('no', 'username', 'password', 'email', 'tel')
    ordering = ('no', )
    form = UserForm
    list_per_page = 10

admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.User, UserAdmin)