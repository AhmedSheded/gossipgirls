from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Poll(models.Model):
    question = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=100)
    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='votes')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('poll', 'voted_by')


class Email(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.subject
