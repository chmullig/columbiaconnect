import json
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.template import Template, RequestContext
from models import *
from django.contrib.auth.models import User

import datetime

def home(request):
	stuff = {"connexes" : Connex.objects.order_by("name")}
	template = 'frontend/index.html'
	if request.user.is_authenticated():
		stuff.update({'logged_in': 'YES'})
	else:
		stuff.update({'logged_in': 'NO'})		
	return render_to_response(template, stuff, context_instance=RequestContext(request))

def login_page(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	print username, password, user, dir(user)

	if user is not None and user.is_authenticated():
		print "logged in"
		login(request, user)
	return redirect('home')

def signup_page(request):
	email = request.POST['email']
	password = request.POST['password_initial']
	password_repeat = request.POST['password_repeat']
	first_name = request.POST['first_name']
	last_name = request.POST['last_name']

	if password == password_repeat:
		user = User.objects.create_user(email, email, password)
		user.first_name = first_name
		user.last_name = last_name
		user.save()		
		now = datetime.datetime.now()
		template = 'frontend/index.html'
	
	return redirect('home')


def logout_page(request):
     logout(request)
     response = redirect('home')
     response.delete_cookie('user_location')
     return response
		
def current_datetime(request):
	now = datetime.datetime.now()
	template = 'dateapp/current_datetime.html'
	return render_to_response(template, {'current_date': now})

def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	
	template = 'dateapp/hours_ahead.html'
	return render_to_response(template, {'offset': offset, 'from_now': dt})
	
	
	"""html = "<html><body> In %s hour(s), it will be %s. </body></html>" % (offset, dt)
	return HttpResponse(html)"""

def query_page(request):
	response_data = {}
	connexes = Connex.objects
	if request.GET.has_key("search"):
		term = request.GET.has_key("search")
		connexes.filter(name__icontains=term)
		response_data["connexes"] = connexes.values_list('name', flat=True)[0]
	return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
	