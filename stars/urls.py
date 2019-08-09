from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from star_wars.views import Home, AddContestan, ListContestan, ListCharacter, DeleteContestan, UpdateContestan, \
    UpdateCharacter
from utils import ajax

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url('home/', Home.as_view(), name='home'),
    url('add_contestan/', AddContestan.as_view(), name='add_contestan'),
    url('list_contestan/', ListContestan.as_view(), name='list_contestan'),
    url('list_character/', ListCharacter.as_view(), name='list_character'),
    url('delete_contestan/(?P<pk>[\d]+)/$', DeleteContestan.as_view(), name='delete_contestan'),
    url('update_contestan/(?P<pk>[\d]+)/$', UpdateContestan.as_view(), name='update_contestan'),
    url('update_character/(?P<pk>[\d]+)/$', UpdateCharacter.as_view(), name='update_character'),

    #Sistema ajax
    url(r'^ajax/get_characters/',ajax.get_character,
        name='get_characters'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
