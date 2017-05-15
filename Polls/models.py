from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

class Survey_Questions(models.Model) :
	question_text = models.CharField(max_length=200)
	when_created = models.DateTimeField(auto_now_add=True)
	multiple_answer = models.BooleanField(default=True)
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
		return self.user_owner.username + " : " + self.question.question_text