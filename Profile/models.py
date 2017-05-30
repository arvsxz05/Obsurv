from django.db import models
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.models import User

def avatar_upload_path(instance, filename):
    return './storage/{}_{}'.format(instance.owner.username, filename)

class User_Profile(models.Model) :
	owner = models.OneToOneField(User, related_name='profile')
	avatar = models.FileField(upload_to=avatar_upload_path, blank=True)

	@property
	def avatar_url(self):
		if self.avatar:
			return self.avatar.url
		return static('img/unknown.gif')

	def __str__(self):
		return self.owner.username