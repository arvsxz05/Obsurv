from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^login/$', views.login_view, name='login'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^(?P<username>[\w@.]+)/$', views.profile_view, name='profile'),
    url(r'^validate-username/$', views.validate_username, name='validate_username'),
    url(r'^edit/(?P<username>[\w@.]+)/$', views.edit_view, name='edit'),
]