from django.conf.urls import url, include

from django.views.generic.base import RedirectView

from .views import (
	UserDetailView,
	UserFollowView,
	)
app_name = 'tweets'

urlpatterns = [
	
        url(r'^(?P<username>[\w.@+-]+)/$',UserDetailView.as_view(), name='detail'), #/tweet/1/
        url(r'^(?P<username>[\w.@+-]+)/follow/$',UserFollowView.as_view(), name='follow'), 

]
