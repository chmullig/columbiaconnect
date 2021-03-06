
import json, os
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.template import Template, RequestContext
from models import *
from django.contrib.auth.models import User
from django.db.models import Q

import datetime

LIMIT = 6

def home(request):
	stuff = {"connexes" : Connex.objects.order_by("?")[:LIMIT]}
	template = 'frontend/index.html'
	if request.user.is_authenticated():
		stuff.update({'logged_in': 'inherit', 'logged_off': 'none', 'user_name':request.user})
	else:
		stuff.update({'logged_in': 'none', 'logged_off': 'inherit'})		
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

def create_groups_page(request):
	stuff = {"categories" : Category.objects.order_by("name")}
	template = 'frontend/create_group.html'

	if request.user.is_authenticated():
		stuff['logged_in'] = 'inherit'
		stuff['logged_off'] = 'none'
		stuff['user_name'] = request.user
	else:
		stuff['logged_in'] = 'none'
		stuff['logged_off'] = 'inherit'

	return render_to_response(template, stuff, context_instance=RequestContext(request))
		
def create_group(request):
	group_name = request.POST['group_name']
	category = request.POST['category']
	description = request.POST['description']
	c = Connex.objects.create()
	c.name = group_name
	c.categories = [Category.objects.get(name=category)]
	c.description = description
	c.save()
	c.users.add(request.user)
	return redirect('home')

def query_page(request):
	response_data = {}
	connexes = Connex.objects
	if request.GET.has_key("search"):
		term = request.GET["search"]
		connexes = connexes.filter(name__icontains=term) | \
				connexes.filter(description__icontains=term)

	if request.GET.has_key("category"):
		catname = request.GET["category"]
		cat = Category.objects.get(name=catname)
		connexes = connexes.filter(categories=cat)

	if request.GET.has_key("sort"):
		sortby = request.GET["sort"]
		if sortby == "Members":
			connexes = connexes.order_by('name')
		elif sortby == "Date":
			connexes = connexes.order_by('datecreated')
		elif sortby == "Random":
			connexes = connexes.order_by('?')

	print connexes
	response_data["connexes"] = list(connexes[:LIMIT].values_list('name', flat=True))
	return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")

def details(request):
	template = 'frontend/groups.html'
	targetPage = request.path[11:]
	print targetPage
	connexes = Connex.objects.filter(name=targetPage)


	if request.user.is_authenticated():
		lin = 'inherit'
		loff = 'none'
		user = request.user
	else:
		lin = 'none'
		loff = 'inherit'
		user = ''

	if(connexes):
		users = connexes[0].users.all()
		members = ""
		for user in users:
			members += (user.email + "\n")
		group_category = connexes[0].categories.values_list
		return render_to_response(template,
				{'group_name':connexes[0].name, 'group_category':group_category,  'group_description':connexes[0].description, 'logged_in':lin, 'logged_off': loff, 'user_name':user, 'members':members}
				, context_instance=RequestContext(request))
	else:
		return redirect('home')


def groupimage(request):
	targetPage = request.path[11:]
	image_data = open("columbiaconnect/static/crown.jpg").read()
	imgfile = "columbiaconnect/static/"+targetPage
	if os.path.exists(imgfile):
		image_data = open(imgfile).read()
	response = HttpResponse(image_data, mimetype="image/jpg")
	return response

	
def users(request):
	template = 'frontend/member.html'	
	targetPage = request.path[7:]
	print targetPage
	users = User.objects.filter(email=targetPage)
	print 

	if request.user.is_authenticated():
		lin = 'inherit'
		loff = 'none'
		user = request.user
	else:
		lin = 'none'
		loff = 'inherit'
		user = ''

	if(users):
		return render_to_response(template, {'member_name':users[0].first_name+" "+users[0].last_name, 'member_email':users[0].email, 'logged_in':lin, 'logged_off': loff, 'user_name':user})
	else:
		return redirect('home')

def join_group(request):
	if request.user.is_authenticated():
		group_name = request.path[12:]
		group = Connex.objects.filter(name = group_name)
		org_site = '/usergroup/' + group_name

		if(group):
			group[0].users.add(request.user)
		
	return redirect(org_site)
