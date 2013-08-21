from django.db import models

# Create your models here.

# class Location(models.Model):
#     pass

class Subject(models.Model):
    """ an experimental subject 

    subjects can have the following:
    - name [CharField] (unique)
    - sex [CharField]

    for consideration:
    - origin (a location, e.g. LAX)
    - acquisiton date
    - history of locations
    - age at acquisition

    """
    name = models.CharField(max_length=255,unique=True)
    desciption = models.TextField(blank=True)
    SEX_CHOICES = (
        ('M', 'male'),
        ('F', 'female'),
        ('U', 'unknown'),
        )
    sex = models.CharField(max_length=1,choices=SEX_CHOICES,default='U')
    origin = models.CharField(max_length=255,blank=True)

    def __unicode__(self):
        return self.name
