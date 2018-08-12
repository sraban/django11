from django.conf.urls import url
from . import views
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

app_name = 'blog'

urlpatterns = [
    url(r'^$',views.index, name="index"),
    url(r'^sraban/$', views.sraban, name='sraban'),
    url(r'^profile/$',TemplateView.as_view(template_name = 'blog/profile.html'), name="profile"),
    url(r'^saved/$', views.SaveProfile, name = 'saved'),
    url(r'^updated/(?P<pk>.*)/$', views.EditProfile, name = 'updated'),
    url(r'^email/(?P<pk>.*)/$', views.emailProfile, name = 'email'),
]