from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    ctc = models.IntegerField()
    stipend = models.IntegerField()
    branches = models.CharField(max_length=50)
    btech_criteria = models.CharField(max_length=50)
    sem_criteria = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    date = models.DateField(default=datetime.now)
    date_of_drive = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class job_profile(models.Model):
    job_profile = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.job_profile


class registered_companies(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    job_profile = models.ForeignKey(
        job_profile, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.company.name}'


class placed_students(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_profile = models.ForeignKey(
        job_profile, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.company.name
