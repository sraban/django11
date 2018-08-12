# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Profile(models.Model):
   name = models.CharField(max_length = 50)
   email = models.CharField(max_length = 50)
   #picture = models.FileField(upload_to = 'pictures') #ImageField
   #document = models.FileField(upload_to = 'documents') #docs
   age = models.IntegerField()
   picture = models.CharField(max_length = 255)
   document = models.TextField(max_length = 255)
   city = models.CharField(max_length = 255)
   gender = models.CharField(max_length = 255)
   banks = models.CharField(max_length = 255)
   summary = models.TextField(max_length = 255)
   banks = models.TextField(max_length = 255)

   def banks_as_list(self):
        return self.banks.split(',')

   def document_as_list(self):
   		return self.document.split(',')

   class Meta:
      db_table = "profile"