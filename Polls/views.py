from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone

from Polls.models import Survey_Questions, Survey_Choices, Responses

def index(request):
	if request.user.is_authenticated :
		context = {
			'questions': Survey_Questions.objects.filter(end_date__gt=timezone.now())
		}
		return render(request, 'homepage.html', context=context)
	return redirect(login_view)

def signup_view(request):
	context = {
		'type': 0,
		'error_message': ""
	}
	if request.method == 'POST':
		username = request.POST['username']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		password = request.POST['password']
		confirm = request.POST['confirm']

		if User.objects.filter(username=username).exists():
			context['error_message'] = "Username already exists"
		if password != confirm :
			context['error_message'] += " Passwords doesnt match"
		context['first_name'] = first_name
		context['last_name'] = last_name

		if context['error_message'] is "" :
			user = User.objects.create_user(username=username, email=email, password=password)
			user.first_name = first_name
			user.last_name = last_name
			user.save()
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('index')

	return render(request, 'login.html', context=context)


def login_view(request):
	if request.user.is_authenticated :
		print(request.user.first_name)
		return redirect('index')
	context = {
		'type': 1
	}

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			context['error_message'] = 'wrong username or password'
			context['username'] = username

	return render(request, 'login.html', context=context)