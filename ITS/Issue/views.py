from django.shortcuts import render , redirect
from django.http import HttpResponse ,HttpResponseRedirect
from .models import User,Issue
from django.utils import timezone
from django.utils import formats
import datetime

def index(request):
	return render(request,'login.html')

def login(request):
	if request.method == 'POST':
		if User.objects.filter(username=request.POST.get('login_username'),password=request.POST.get('login_password')).count()!=0:
			request.session['username']=request.POST.get('login_username')
			k=User.objects.filter(username=request.POST.get('login_username'),password=request.POST.get('login_password'))
			if k[0].user_type==1:
				request.session['user_type']=1
				return redirect(show)
			else:
				request.session['user_type']=0	
				return redirect(find)
		else :
			return render(request,'login.html')
	else :
		if 'username' in  request.session :
			if request.session['user_type']==0:
				return redirect(find)
			else:
				return redirect(show)
		else :
			return render(request,'login.html')


def find(request):
	if 'username'  in  request.session :
		if request.session['user_type']==0:
			v=User.objects.get(username=request.session['username'])
			l = v.issuer.exclude(issue_user_close=1)
			context = {'username' : request.session['username'] ,'Issues' : l}
			return render(request,'find.html',context)
		else:
			return redirect(show)
	else :
		return redirect(index)	


def show(request):
	if 'username'  in  request.session :
		if request.session['user_type']==0:
			return redirect(find)
		else:
			l = Issue.objects.exclude(issue_user_close=1)
			context = {'username' : request.session['username'] ,'Issues' : l}
			return render(request,'show.html',context)
	else :
		return redirect(index)	


def logout(request):
	del request.session['username']
	return redirect(login)


def remove(request):
	if 'username'  in  request.session :
		if request.method == 'POST':
			I=Issue.objects.filter(id=int(request.POST.get('id'))).update(
			issue_close_date=timezone.now()
			,issue_user_close=1)
			
			return HttpResponseRedirect('/Issue/find/')
		else :
			return HttpResponseRedirect('/Issue/find/')
	else :
		return HttpResponseRedirect('/Issue/home/')

def submit(request):
	if 'username'  in  request.session :
		if request.method == 'POST':
			if request.POST.get('type_issue')!=None or request.POST.get('type')!=None :
				o=Issue(type_issue=request.POST.get('type'),issue=request.POST.get('issue'),issue_open_date=timezone.now(),issue_close_date=timezone.now())
				o.complainer=User.objects.get(username=request.session['username'])
				o.save()
				return HttpResponseRedirect('/Issue/find/')
			else:
				return HttpResponseRedirect('/Issue/find/')
		else:
			return HttpResponseRedirect('/Issue/find/')
	else :
		return HttpResponseRedirect('/Issue/home/')	

# Create your views here.
