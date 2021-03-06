import re
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from .validators import validate_content
from django.urls import reverse
from django.utils import timezone
from hashtags.signals import parsed_hashtags

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


# Create your models here.
class TweetManager(models.Manager):
	def retweet(self, user, parent_obj):
		if parent_obj.parent:
			og_parent = parent_obj.parent 		#og_parent = original parent
		else:
			og_parent = parent_obj

		qs = self.get_queryset().filter(
			user=user, parent=og_parent
			).filter(
				timestamp__year=timezone.now().year,
				timestamp__month=timezone.now().month,
				timestamp__day=timezone.now().day,
				reply=False,
			)
		if qs.exists():
			return None

		obj = self.model(
				parent  = og_parent,
				user    = user,
				content = parent_obj.content,
			)
		obj.save()
		return obj

	def like_toggle(self, user, tweet_obj):
		if user in tweet_obj.liked.all():
			is_liked = False
			tweet_obj.linked.remove(user)
		else:
			is_liked = True
			tweet_obj.linked.add(user)
		return is_liked


class Tweet(models.Model):
	parent		= models.ForeignKey(
							"self",
							blank=True,
							null=True,
							on_delete=models.CASCADE,
							)
	user		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user),)
	content 	= models.CharField(max_length=120, validators=[validate_content])
	liked		= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
	reply		= models.BooleanField(verbose_name='Is a reply?', default=False)
	updated 	= models.DateTimeField(auto_now=True)
	timestamp   = models.DateTimeField(auto_now_add=True)

	objects = TweetManager()

	
	def __str__(self):
		return str(self.content)

	def get_absolute_url(self):
		return reverse("tweet:detail", kwargs={"pk":self.pk})

	class Meta:
		ordering = ['-timestamp']

	def get_parent(self):
		the_parent = self
		if self.parent:
			the_parent = self.parent
		return the_parent

	def get_children(self):
		parent = self.get_parent()
		qs = Tweet.objects.filter(parent=parent)
		qs_parent = Tweet.objects.filter(pk=parent.pk)
		return (qs | qs_parent)


def tweet_save_receiver(sender, instance, created, *args, **kwargs):
	if created and not instance.parent:
		user_regex = r'@(?P<username>[\w.@+-]+)'
		usernames = re.findall(user_regex, instance.content)

		#send notifications

		hash_regex = r'#(?P<hashtag>[\w\d-]+)'
		hashtags = re.findall(hash_regex, instance.content)
		parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)

		#send hashtags notifications to the user



post_save.connect(tweet_save_receiver, sender=Tweet)
