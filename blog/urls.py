from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from blog import views
from django.conf import settings

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('details/<int:pk>', views.details, name='detail'),
    url(r'mdeditor/', include('mdeditor.urls')),
    path('show_archives/', views.archives, name='archives'),
    path('archives/<int:year>/<int:month>/', views.ArchivesView.as_view(), name='archive'),
    path('show_categories', views.categories, name='categories'),
    path('categories/<int:pk>/', views.CategoriesView.as_view(), name='category'),
    path('show_tages', views.tags, name='tags'),
    path('tag/<int:pk>', views.TagsView.as_view(), name='tag'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
