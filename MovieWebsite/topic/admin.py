from django.contrib import admin
from .models import Topic, TopicPost, TopicMemberShip

admin.site.register(Topic)
admin.site.register(TopicPost)
admin.site.register(TopicMemberShip)
