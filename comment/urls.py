from django.urls import path, include
from comment import views
app_name = 'comment'

urlpatterns = [
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
]