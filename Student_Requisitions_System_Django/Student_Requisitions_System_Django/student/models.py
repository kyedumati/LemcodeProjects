from django.db import models

# Create your models here.


class Faculty(models.Model):
    name = models.CharField(max_length=50)
    facid = models.CharField(max_length=6, primary_key=True)
    dept = models.CharField(max_length=4)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=255, unique=True)


class Student(models.Model):
    name = models.CharField(max_length=50)
    usn = models.CharField(max_length=10, primary_key=True)
    dept = models.CharField(max_length=4)
    facid = models.ForeignKey(Faculty, related_name='faculties', on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=255, unique=True)


class Office(models.Model):
    name = models.CharField(max_length=50)
    office_id = models.CharField(max_length=10, primary_key=True)
    office_section = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=255, unique=True)


class Requisitions(models.Model):
    name = models.CharField(max_length=50)
    usn = models.ForeignKey(Student, on_delete=models.CASCADE)
    facid = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    reqid = models.CharField(max_length=7, primary_key=True)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=255)
    date = models.DateTimeField()
    subject = models.TextField(max_length=50)
    office_section = models.TextField(max_length=30)
    issue = models.TextField(max_length=30)
    reason = models.TextField(max_length=100)
    proc_appr = models.PositiveIntegerField(default=0)
    hod_appr = models.PositiveIntegerField(default=0)
    office_appr = models.PositiveIntegerField(default=0)

