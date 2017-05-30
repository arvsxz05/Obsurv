from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^question-view/(?P<question_id>\d+)$', views.question_view, name='question'),
    url(r'^respond/(?P<question_id>\d+)$', views.respond, name='respond'),
    url(r'^get-answers/(?P<question_id>\d+)$', views.get_answers, name='get_answers'),
]