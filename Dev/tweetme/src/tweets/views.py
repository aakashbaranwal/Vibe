from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin
from django.db.models import Q
from .mixins import UserOwnerMixin
from django.urls import reverse_lazy, reverse
from .models import Tweet
from django.views import View
from django.http import HttpResponseRedirect
# Create Data

class RetweetView(View):
	def get(self, request, pk, *args, **kwargs):
		tweet = get_object_or_404(Tweet, pk=pk)
		if request.user.is_authenticated:
			new_tweet = Tweet.objects.retweet(request.user, tweet)
	#		return HttpResponseRedirect(tweet.get_absolute_url())
			return HttpResponseRedirect("/")
		return HttpResponseRedirect(tweet.get_absolute_url())



class TweetCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = 'tweets/create_view.html'
	#success_url = reverse_lazy("tweet:detail")
	#success_url = "/tweet/"							#THIS TAKES US TO THE PAGE WHEN THE ACTION IS A SUCCESS
	login_url = '/admin/'						# THIS IS FOR THE USER AUTHENTICATION PART WHEN A USER TRIES TO UPDATE OR DELETE SOME STUFF (HERE TWEET)

# Update Data

class  TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
	queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = 'tweets/update_view.html'
	success_url = "/tweet/"						#THIS TAKES US TO THE PAGE WHEN THE ACTION IS A SUCCESS
	login_url = '/admin/'					# THIS IS FOR THE USER AUTHENTICATION PART WHEN A USER TRIES TO UPDATE OR DELETE SOME STUFF (HERE TWEET)

# Retreive Data

class TweetDeleteView(LoginRequiredMixin, DeleteView):
	queryset = Tweet.objects.all()
	template_name = 'tweets/delete_confirm.html'
	model = Tweet
	success_url = reverse_lazy("tweet:list")
	#success_url = "/tweet/"   #THIS TAKES US TO THE PAGE WHEN THE ACTION IS A SUCCESS
	login_url = '/admin/'				   # THIS IS FOR THE USER AUTHENTICATION PART WHEN A USER TRIES TO UPDATE OR DELETE SOME STUFF (HERE TWEET)

class TweetDetailView(DetailView):
	queryset = Tweet.objects.all()

class TweetListView(LoginRequiredMixin, ListView):

	def get_queryset(self, *args, **kwargs):
		qs = Tweet.objects.all()
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter(
					Q(content__icontains=query) |
					Q(user__username__icontains=query)
					)
		return qs
	


	def get_context_data(self, *args, **kwargs):
		context = super(TweetListView, self).get_context_data(*args, **kwargs)
		context['create_form'] = TweetModelForm()
		context['create_url'] = reverse_lazy("tweet:create")
		return(context)