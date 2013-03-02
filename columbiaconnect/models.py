from django.db import models
from django.contrib.auth.models import Group, User

class UserManager(models.Manager):
    def get_query(self):
        return super(UserManager, self).get_query_set().distinct()

class Student(models.Model):
    user = models.OneToOneField(User)
    classyear = models.CharField(max_length=10)


#posts/announcements
#events?
#users in groups