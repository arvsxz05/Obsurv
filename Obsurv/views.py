from django.shortcuts import render, redirect, reverse
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
from django.utils import timezone
from django.core.paginator import Paginator
import datetime

from Polls.models import Survey_Questions, Survey_Choices, Responses
from Profile.models import User_Profile

def index(request, page_num):
	if not request.user.is_authenticated :
		return redirect(login_view)

	user_on_question=Responses.objects.filter(
		question=OuterRef('pk'),
		user_owner__username=request.user.username
	)

	questions = []
	question_objects = Survey_Questions.objects.all().annotate(
		respondent_count=Count('Responses__user_owner', distinct=True)
	).annotate(
		answered=Exists(user_on_question)
	).all().order_by("-when_created").filter(end_date__gt=timezone.now())

	p = Paginator(question_objects, 4)
	try:
		page_num = int(page_num)
	except ValueError:
		page_num = 1
	if page_num:
		if page_num > p.num_pages and page_num < p.num_pages:
			return redirect('page_404')
		question_objects = p.page(page_num)
	else:
		question_objects = p.page(1)

	for question in zip(*[iter(question_objects)]*2):
		questions.append(question)
	if len(question_objects)%2 == 1 :
		questions.append((question_objects[len(question_objects)-1], None))

	context = {
		'username': request.user.username,
		'questions': questions,
		'colors': Survey_Questions.COLOR_PALLETE,
		'pages': question_objects,
		'current': page_num
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

		color = request.POST.get('color')

		question_object = Survey_Questions.objects.create(user_owner=request.user, question_text=question, multiple_answer=multiple, end_date=end_datetime, card_color=color)
		for choice in choices:
			Survey_Choices.objects.create(question=question_object, choice_text=choice)

		return redirect('index')
	return render(request, 'homepage.html', context=context)