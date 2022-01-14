from django.urls import path
from django.urls.conf import path, re_path
from women.views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('cats/<int:catid>/', categories),
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive)
]
