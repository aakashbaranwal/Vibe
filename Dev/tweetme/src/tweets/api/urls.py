from django.conf.urls import url

from django.views.generic.base import RedirectView

from .views import (
	LikeToggleAPIView,
	RetweetAPIView,
	TweetListAPIView,
	TweetCreateAPIView,
	TweetDetailAPIView,
	)

app_name = 'tweets'

urlpatterns = [

        url(r'^$', TweetListAPIView.as_view(), name='list'), # /api/tweet/
        url(r'^create/$', TweetCreateAPIView.as_view(), name='create'), # /api/tweet/create/
        url(r'^(?P<pk>\d+)/$', TweetDetailAPIView.as_view(), name='detail'), # /api/tweet/
        url(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='like-toggle'), # /api/tweet/
        
        url(r'^(?P<pk>\d+)/retweet/$', RetweetAPIView.as_view(), name='retweet'), # /api/tweet/


]
