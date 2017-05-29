from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.defaults import page_not_found

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^(?P<username>\w+)/$', views.profile_view, name='profile'),
    url(r'^validate-username/$', views.validate_username, name='validate_username'),
    url(r'^edit/(?P<username>\w+)$', views.edit_view, name='edit'),
    url(r'^respond/(?P<question_id>\d+)$', views.respond, name='respond'),
    url(r'^get-answers/(?P<question_id>\d+)$', views.get_answers, name='get_answers'),
    url(r'^404/$', page_not_found, name="page_404"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)