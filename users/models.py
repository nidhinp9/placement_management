from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usn = models.CharField(max_length=100, unique=True)
    phoneNo = models.CharField(max_length=10)
    backlogs = models.IntegerField(default=0)
    branch = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Past_Education_Details(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tenth_scheme = models.CharField(max_length=100)
    twelve_scheme = models.CharField(max_length=100)
    cet_rank = models.CharField(max_length=100)
    tenth_percentage = models.FloatField()
    twelve_percentage = models.FloatField()


class Current_Education_Details(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    first_sem_sgpa = models.FloatField(blank=True, null=True)
    second_sem_sgpa = models.FloatField(blank=True, null=True)
    third_sem_sgpa = models.FloatField(blank=True, null=True)
    fourth_sem_sgpa = models.FloatField(blank=True, null=True)
    fifth_sem_sgpa = models.FloatField(blank=True, null=True)
    sixth_sem_sgpa = models.FloatField(blank=True, null=True)
    seventh_sem_sgpa = models.FloatField(blank=True, null=True)
    eighth_sem_sgpa = models.FloatField(blank=True, null=True)


class Other_Details(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.CharField(max_length=300)
    dob = models.DateField()
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('profile')
