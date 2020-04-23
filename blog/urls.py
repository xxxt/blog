from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from blog import views
from django.conf import settings

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('details/<int:pk>/', views.details, name='details'),
    url(r'mdeditor/', include('mdeditor.urls')),
    path('show_archives/', views.archives, name='archives'),
    path('archives/<int:year>/<int:month>/', views.ArchivesView.as_view(), name='archive'),
    path('show_categories/', views.categories, name='categories'),
    path('categories/<int:pk>/', views.CategoriesView.as_view(), name='category'),
    path('show_tages/', views.tags, name='tags'),
    path('tag/<int:pk>', views.TagsView.as_view(), name='tag'),
    # path('search', views.SearchView.as_view(), name='search'),
    path('search/', views.search, name='search'),
    path('create/', views.article_create, name='create'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('captcha/', views.get_captcha),
    path('increase-likes/<int:id>/', views.IncreaseLikesView.as_view(), name='increase_likes'),
    path('about/', views.about, name='about'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
