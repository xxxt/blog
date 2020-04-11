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
    path('archives/', views.archives, name='archives'),
    path('archives/<int:year>/<int:month>/', views.ArchivesView.as_view(), name='archive'),
    path('categories', views.categories, name='categories'),
    path('categories/<int:pk>/', views.categories_detail, name='category'),
    path('tages', views.tags, name='tags'),
    path('tag/<int:pk>', views.tags_detail, name='tag'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
