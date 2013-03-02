
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.template import Template, RequestContext

import datetime

def home(request):
	if request.user.is_authenticated():
		now = datetime.datetime.now()
		template = 'frontend/index.html'
		return render_to_response(template, {'current_date': now,'logged_in': 'YES'}, context_instance=RequestContext(request))
	else:
		now = datetime.datetime.now()
		template = 'frontend/index.html'
		return render_to_response(template, {'current_date': now,'logged_in': 'NO'}, context_instance=RequestContext(request))

def login_page(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	print username, password, user, dir(user)

	if user.is_authenticated():
		print "logged in"
		login(request, user)
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
