from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import json


class Rider(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=30, null=True)
    nickname = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_rider(cls, id):
        return cls.objects.get(user_id=id)

    @classmethod
    def to_json(cls, riders):
        context = []
        for rider in riders:
            json_rider = {
                'id': rider.user.id,
                'username': rider.user.username,
                'email': rider.user.email,
                'first_name': rider.first_name,
                'nickname': rider.nickname,
                'last_name': rider.last_name
            }
            context.append(json_rider)
        return json.dumps(context)


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

    @classmethod
    def get_event(cls, event_id):
        return cls.objects.get(id=event_id)

    def __str__(self):
        return '{} - Кога: {}, Къде: {}, Какво: {}'.format(self.name, self.date, self.start_point, self.description)

    @classmethod
    def to_json(cls, events):
        context = []
        for event in events:
            json_event = {
                'name': event.name,
                'date': str(event.date),
                'start_point': event.start_point,
                'start_point_coordinates': event.start_point_coordinates,
                'end_point': event.end_point,
                'end_point_coordinates': event.end_point_coordinates,
                'description': event.description,
                'noob_friendly': event.noob_friendly,
                'creator': event.creator.username
            }
            context.append(json_event)
        return json.dumps(context)


class Comment(models.Model):
    event = models.ForeignKey(Event)
    poster = models.ForeignKey(User)
    content = models.TextField()
    reply = models.ForeignKey("self", null=True)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_comment(cls, comment_id):
        return cls.objects.get(id=comment_id)

    @classmethod
    def to_json(cls, comments):
        context = []
        for comment in comments:
            json_comment = {
                'event': comment.event.name,
                'poster': comment.poster.username,
                'id': comment.id,
                'comment': comment.content,
                'reply': comment.reply_id
            }
            context.append(json_comment)
        return json.dumps(context)
