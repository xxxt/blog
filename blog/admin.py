from django.contrib import admin

# Register your models here.

from blog import models
# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'visiting', 'created_time', 'modifyed_time')
    # ordering = ('visiting', )


admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Blog, BlogAdmin)
