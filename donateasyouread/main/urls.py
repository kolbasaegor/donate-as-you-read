from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('blog/', RenderBlog.as_view(), name='blog'),
    path('blog/<slug:slug>', RenderArticle.as_view(), name='article'),
    path('donate/', donate, name='donate'),
    path('register/', register_form, name='register'),
    path('login/', login_form, name='login'),
    path('logout/', logout, name='logout'),
    path('write-article/', write_article, name='write-article'),
    path('about/', about, name='about'),
    path('user/<str:username>', render_user, name='user')
]