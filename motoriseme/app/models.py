from django.db import models
from django.contrib.auth.models import User

class Rider(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	first_name = models.CharField(max_length=30, null=True)
	nickname = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
