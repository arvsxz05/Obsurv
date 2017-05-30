from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Exists, OuterRef
from django.utils import timezone

from Polls.models import Survey_Questions, Survey_Choices, Responses
from Profile.models import User_Profile

def respond (request, question_id) :
	question_responded = get_object_or_404(Survey_Questions, id=question_id)

	if not request.user.is_authenticated:
		return redirect(login_view)

	question_responded.Responses.filter(user_owner=request.user).delete()

	response = request.GET.getlist('response[]')
	for single_choice in response:
		choice = Survey_Choices.objects.get(pk=single_choice)
		Responses.objects.create(question=question_responded, choice=choice, user_owner=request.user)
	data = {
		'success': True,
		'question': question_id,
		'no_respondents': len(question_responded.Responses.values_list('user_owner', flat=True).distinct())
	}
	return JsonResponse(data)

def get_answers (request, question_id) :
	question_answered = get_object_or_404(Survey_Questions, id=question_id)

	if not request.user.is_authenticated:
		return redirect(login_view)

	data = {
		'answers': list(question_answered.Responses.filter(user_owner__username=request.user.username).values_list('choice_id', flat=True))
	}
	return JsonResponse(data)

def question_view(request, question_id):
	question = get_object_or_404(Survey_Questions, id=question_id)
	context = {
		"question": question,
		"choices": question.Choices.all(),
		"username": request.user.username
	}
	return render(request, 'questions.html', context=context)
