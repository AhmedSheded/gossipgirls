from django.contrib import admin
from .models import Poll, Choice, Vote, Email
# Register your models here.

admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Vote)
admin.site.register(Email)