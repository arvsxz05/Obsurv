from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your models here.

class Survey_Questions(models.Model) :
	question_text = models.CharField(max_length=200)
	when_created = models.DateTimeField(auto_now_add=True)
	multiple_answer = models.BooleanField(default=False)
	user_owner = models.ForeignKey(User, related_name='Surveys')
	no_of_respondents = models.IntegerField(default=0)
	end_date = models.DateTimeField()

	def clean(self):
		if self.end_date is None or self.end_date <= timezone.now():
			raise ValidationError('End Date and Time should be later than the Date and Time the survey was created.')

	def __str__(self):
		return self.question_text

class Survey_Choices(models.Model) :
	question = models.ForeignKey(Survey_Questions, related_name='Choices')
	choice_text = models.CharField(max_length=100)

	def __str__(self):
		return self.choice_text

class Responses(models.Model) :
	question = models.ForeignKey(Survey_Questions, related_name='Responses')
	choice = models.ForeignKey(Survey_Choices)
	user_owner = models.ForeignKey(User, related_name='Responses')

	def __str__(self):
		return self.user_owner.username + " : " + self.question.question_text + " : " + self.choice.choice_text

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