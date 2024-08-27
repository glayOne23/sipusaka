"""Module"""

from django.contrib import admin
from django.urls import path, include

from apps.landingpage.views import home, journal, article

app_name = 'landingpage'

urlpatterns = [
    path('admin/', admin.site.urls),
	path('',      home.home,       name='home'),
    path('journal/', include([
        path('', journal.index, name='journal.index'),
        path('<int:journal_id>/article/', article.index, name='article.index'),
        # path('<int:id>/baca_pdf', buku.baca_pdf, name='buku.baca_pdf'),
    ])),
#   path('404',   home.error_404,  name='404')
]
