
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.loader import get_template
import datetime

def home(request):
	now = datetime.datetime.now()
	template = 'frontend/index.html'
	return render_to_response(template, {'current_date': now})
	
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