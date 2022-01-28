from django.urls.conf import path
from .views import *

urlpatterns = [
    path('', WomenHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:slug>/', WomenCategory.as_view(), name='category'),
    # re_path(r'^archive/(?P<year>[0-9]{4})/', archive)
]
