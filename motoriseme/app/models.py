from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Rider(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	first_name = models.CharField(max_length=30, null=True)
	nickname = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)


class Event(models.Model):
    name = models.CharField(max_length = 100)
    date = models.DateTimeField(default = datetime.now())
    start_point = models.CharField(max_length = 254)
    start_point_coordinates = models.CharField(max_length = 100)
    end_point = models.CharField(max_length = 254)
    end_point_coordinates = models.CharField(max_length = 100)
    description = models.CharField(max_length = 254)
    noob_friendly = models.BooleanField(default = False)
    creator = models.ForeignKey(User)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    def __str__(self):
        return '{} - Кога: {}, Къде: {}, Какво: {}'.format(self.name, self.date, self.start_point, self.description)
