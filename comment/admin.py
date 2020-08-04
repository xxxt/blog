from django.contrib import admin
# Register your models here.

from comment import models
# from blog.forms import UserForm
# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'body', 'created')


admin.site.register(models.Comment)
admin.site.register(models.Comment, CommentAdmin)
