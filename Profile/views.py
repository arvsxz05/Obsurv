from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from Profile.forms import UserInfoForm
from django.db.models import Count
from django.db.models import Exists, OuterRef
from django.utils import timezone

from Polls.models import Survey_Questions, Survey_Choices, Responses
from Profile.models import User_Profile

def signup_view(request):
	context = {
		'type': 0,
		'sign_error_message': ""
	}
	if request.method == 'POST':
		username = request.POST['username']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		password = request.POST['password']
		confirm = request.POST['confirm']

		if User.objects.filter(username=username).exists():
			context['sign_error_message'] = "Username already exists"
		if password != confirm :
			context['sign_error_message'] += " Passwords doesnt match"
		context['first_name'] = first_name
		context['last_name'] = last_name

		if context['sign_error_message'] is "" :
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
		return redirect(reverse('profile', kwargs={"username":request.user.username}))
	context = {
		'type': 1
	}

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect(reverse('profile', kwargs={"username":username}))
		else:
			context['error_message'] = 'wrong username or password'
			context['username'] = username

	return render(request, 'login.html', context=context)

def logout_view(request):
	logout(request)
	return redirect(login_view)

def profile_view (request, username):
	if not request.user.is_authenticated:
		return redirect ('login')
	user = get_object_or_404(User, username=username)
	
	user_on_question=Responses.objects.filter(
		question=OuterRef('pk'),
		user_owner__username=request.user.username
	)

	questions = []
	question_objects = Survey_Questions.objects.all().annotate(
		respondent_count=Count('Responses__user_owner', distinct=True)
	).annotate(
		answered=Exists(user_on_question)
	).all().order_by("-when_created").filter(end_date__gt=timezone.now(), user_owner=user)

	for question in zip(*[iter(question_objects)]*2):
		questions.append(question)
	if len(question_objects)%2 == 1 :
		questions.append((question_objects[len(question_objects)-1], None))

	context = {
		'username': request.user.username,
		'user': user,
		'questions': questions,
		'colors': Survey_Questions.COLOR_PALLETE
	}

	return render(request, 'profile.html', context=context)

def validate_username(request):
    username = request.GET.get('username', None)
    print ("here")
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def edit_view (request, username):
	if not request.user.is_authenticated :
		return redirect(login_view)

	if request.user.username != username :
		return redirect(reverse('page_404'))

	if request.method == 'POST':
		form = UserInfoForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect(reverse('profile', kwargs={'username': request.user.username}))
	else:
		form = UserInfoForm(instance=request.user)

	context = {
		'form': form,
		'username': request.user.username
	}
	return render(request, 'edit_profile.html', context=context)
