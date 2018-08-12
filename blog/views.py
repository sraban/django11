# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core import serializers
import requests
import json
import os
import time
import datetime

from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect

from blog.models import Profile
from blog.forms import ProfileForm
from django.conf import settings

# Create your views here.
def sraban(request):
	data = requests.get('https://sraban.000webhostapp.com/')
	return HttpResponse(data)

def save_file(file, path):
    ''' Little helper to save a file '''
    fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path)), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()
    return True

def emailProfile(request, pk):

   detail = Profile.objects.get( pk = pk )
   html_content = render(request,'blog/email_profile.html', locals())
   html_content = str(html_content).replace('Content-Type: text/html; charset=utf-8','').replace('\n','')
   emailto = detail.email
   email = EmailMessage("my subject", html_content, "from@edkal.com", [emailto])
   email.content_subtype = "html"
   res = email.send()
   return HttpResponse('%s'%res)

def index(request):
   deleted = False
   detail = Profile.objects.all()
   if request.method == "POST":
   	if 'delete_id' in request.POST:
   	 delete_id = request.POST['delete_id']
        try:
         Profile.objects.get( pk = delete_id ).delete()
         deleted = True
        except Profile.DoesNotExist:
         deleted = False
   return render(request, 'blog/list_profile.html', locals())

def SaveProfile(request):
   
   saved = False
   document_files = []

   if request.method == "POST":
   	
      MyProfileForm = ProfileForm(request.POST, request.FILES)
      
      if MyProfileForm.is_valid():
         profile = Profile() 
         #MyProfileForm.cleaned_data["agree"]
         #profile.picture = MyProfileForm.cleaned_data["picture"]
         if 'name' in request.POST:
         	profile.name = MyProfileForm.cleaned_data["name"]
         if 'email' in request.POST:
         	profile.email = MyProfileForm.cleaned_data["email"]
         if 'city' in request.POST:
         	profile.city = request.POST["city"]
         if 'gender' in request.POST:
         	profile.gender = request.POST["gender"]
         if 'age' in request.POST:
         	profile.age = request.POST["age"]
         if 'summary' in request.POST:
         	profile.summary = request.POST["summary"]
         
         if 'picture' in request.FILES:
         	ts = time.time()
         	pic_name = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S_') + request.FILES['picture']._get_name()
         	pic_name = 'static/pictures/' + pic_name.replace(' ', '_').lower()
         	if save_file(request.FILES['picture'], pic_name):
         		profile.picture = pic_name

         if 'documents' in request.FILES:
            ts = time.time()
            for document in request.FILES.getlist('documents'):
             document_file = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S_') + document._get_name()
             document_file = 'static/documents/' + document_file.replace(' ', '_').lower()
             if save_file(document, document_file):
              document_files.append(document_file)
            if len(document_files) > 0:
             profile.document = ','.join(document_files)
            
         if request.POST.has_key('bank'):
            profile.banks = ','.join(request.POST.getlist('bank')) 
         
         profile.save()
         saved = True
   else:
      MyProfileForm = ProfileForm()
	
   #return HttpResponse(profile.document)
   #return HttpResponse(json.dumps(request.POST))
   #return HttpResponseRedirect('/thanks/') # Redirect
   return render(request, 'blog/profile.html', locals())


def EditProfile(request, pk):
   document_files = []
   detail = Profile.objects.get( pk = pk )
   saved = False
   if request.method == "POST":

      MyProfileForm = ProfileForm(request.POST, request.FILES)
      
      if MyProfileForm.is_valid():
         #MyProfileForm.cleaned_data["agree"]
         #profile.picture = MyProfileForm.cleaned_data["picture"]
         if 'name' in request.POST:
         	detail.name = MyProfileForm.cleaned_data["name"]
         if 'email' in request.POST:
         	detail.email = MyProfileForm.cleaned_data["email"]
         if 'city' in request.POST:
         	detail.city = request.POST["city"]
         if 'gender' in request.POST:
         	detail.gender = request.POST["gender"]
         if 'age' in request.POST:
         	detail.age = request.POST["age"]
         if 'summary' in request.POST:
         	detail.summary = request.POST["summary"]
         
         if 'picture' in request.FILES:
         	ts = time.time()
         	pic_name = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S_') + request.FILES['picture']._get_name()
         	pic_name = 'static/pictures/' + pic_name.replace(' ', '_').lower()
         	if save_file(request.FILES['picture'], pic_name):
         		detail.picture = pic_name

         if 'documents' in request.FILES:
            ts = time.time()
            for document in request.FILES.getlist('documents'):
             document_file = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S_') + document._get_name()
             document_file = 'static/documents/' + document_file.replace(' ', '_').lower()
             if save_file(document, document_file):
              document_files.append(document_file)
            if len(document_files) > 0:
             detail.document = ','.join(document_files)

         if request.POST.has_key('bank'):
            detail.banks = ','.join(request.POST.getlist('bank')) 

         detail.save()
         saved = True
   else:
      MyProfileForm = ProfileForm()
	
   #return HttpResponse(detail.city)
   #return HttpResponse(json.dumps(document_files))
   #return HttpResponseRedirect('/thanks/') # Redirect
   return render(request, 'blog/edit_profile.html', locals())

