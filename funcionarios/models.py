from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Employee(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, default=name)
    role = models.CharField(max_length=255)
    salary = models.PositiveIntegerField()
    work_section = models.CharField(max_length=255)
    

    def __str__(self):
        return self.name

class TimeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

class Ferias(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=(('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')), default='Pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.start_date} to {self.end_date}"