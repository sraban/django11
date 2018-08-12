#-*- coding: utf-8 -*-
from django import forms
from blog.models import Profile

class ProfileForm(forms.Form):
   name = forms.CharField(max_length = 50)
   email = forms.EmailField(max_length = 50)
   #picture = forms.FileField()
   #documents = forms.FileField()