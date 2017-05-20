from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from Polls.forms import UserInfoForm
from django.db.models import Count
from django.utils import timezone
import datetime

from Polls.models import Survey_Questions, Survey_Choices, Responses

def index(request):
	if not request.user.is_authenticated :
		return redirect(login_view)

	questions = []
	question_objects = Survey_Questions.objects.all().annotate(respondent_count=Count('Responses__user_owner', distinct=True)).all().order_by("-when_created").filter(end_date__gt=timezone.now()).order_by("-when_created").prefetch_related('Choices')
	for question in zip(*[iter(question_objects)]*2):
		questions.append(question)
	if len(question_objects)%2 == 1 :
		questions.append((question_objects[len(question_objects)-1], None))

	context = {
		'username': request.user.username,
		'questions': questions
	}

	if request.method == "POST":
		question = request.POST.get('question')
		# in case the no_of_choices field is not recognizable or not in integer form
		try:
			no_of_choices = int(request.POST.get('no_of_choices'))
		except ValueError:
			context["question"] = question
			context['error'] = "Please include a question and 2 or more choices."
			return render(request, "homepage.html", context=context)

		# if the number of choices on the form is less than 2

		if no_of_choices < 2:
			context["question"] = question
			context['error'] = "Please include 2 or more choices."
			return render(request, "homepage.html", context=context)

		# we store in an array all the choices in the form, the number which was indicated by the no_of_choices field
		i = 0
		choices = [None]*no_of_choices
		while i < no_of_choices:
			name_str = 'id' + str(i)
			choices[i] = request.POST.get(name_str)
			i += 1

		# if the user opted to make the survey answerable by one or may choices
		multiple = request.POST.get("multiple")
		multiple = True if multiple == "on" else False

		# if there is no end date provided
		if request.POST.get("end_date") == None or request.POST.get("end_date") == "":
			context["question"] = question
			context['error'] = "Please include an end date."
			return render(request, "homepage.html", context=context)

		# get the equivalent date and time for the string input of the template
		end_date = datetime.datetime.strptime(request.POST.get("end_date"), "%d %B, %Y").date()
		end_time = datetime.datetime.strptime(request.POST.get("end_time"), "%I:%M%p").time()
		end_datetime = datetime.datetime.combine(end_date, end_time)

		# if the timestamp provided is earlier than the poll was created
		if end_datetime < datetime.datetime.now():
			context["question"] = question
			context['error'] = datetime.datetime.now()
			return render(request, 'homepage.html', context=context)

		question_object = Survey_Questions.objects.create(user_owner=request.user, question_text=question, multiple_answer=multiple, end_date=end_datetime)
		for choice in choices:
			Survey_Choices.objects.create(question=question_object, choice_text=choice)

		return redirect('index')
	return render(request, 'homepage.html', context=context)
	

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
	context = {
		'username' : user.username
	}
	return render(request, 'profile.html', context=context)

def validate_username(request):
    username = request.GET.get('username', None)
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

def respond (request, question_id) :
	question_responded = get_object_or_404(Survey_Questions, id=question_id)

	if not request.user.is_authenticated:
		return redirect(login_view)

	response = request.GET.getlist('response[]')
	print (response)
	data = {
		'success': True,
		'question': question_id,
		'no_respondents': question_responded.no_of_respondents+1
	}
	return JsonResponse(data)
	# return redirect(reverse('profile', kwargs={'username': request.user.username}))

	

# def post_poll(request):
# 	if not request.user.is_authenticated:
# 		return redirect ('login')
# 	context = {}
# 	if request.method == "POST":
# 		question = request.POST.get('question')
# 		context["question"] = question
# 		try:
# 			no_of_choices = int(request.POST.get('no_of_choices'))
# 		except ValueError:
# 			context['error'] = "Please include a question and 2 or more choices."
# 			return render(request, "homepage.html", context=context)
# 		if no_of_choices < 2:
# 			context['error'] = "Please include a question and 2 or more choices."
# 			return render(request, "homepage.html", context=context)
# 		i = 0
# 		choices = [None]*no_of_choices
# 		while i < no_of_choices:
# 			name_str = 'id' + str(i)
# 			choices[i] = request.POST.get(name_str)
# 			i += 1
# 		multiple = request.POST.get("multiple")
# 		multiple = True if multiple == "on" else False
# 		end_date = datetime.datetime.strptime(request.POST.get("end_date"), "%d %B, %Y").date()
# 		end_time = datetime.datetime.strptime(request.POST.get("end_time"), "%I:%M%p").time()
# 		end_datetime = datetime.datetime.combine(end_date, end_time)
# 		if end_datetime < datetime.datetime.now():
# 			context['error'] = datetime.datetime.now()
# 			return render(request, 'homepage.html', context=context)
# 		question_object = Survey_Questions.objects.create(user_owner=request.user, question_text=question, multiple_answer=multiple, end_date=end_datetime)
# 		for choice in choices:
# 			Survey_Choices.objects.create(question=question_object, choice_text=choice)
# 	return redirect('index')