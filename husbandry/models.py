from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField(blank=True)


    def __unicode__(self):
        return self.name

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
    origin = models.ForeignKey(Location,null=True,related_name='subjects_from_here')

    def __unicode__(self):
        return self.name

class Record(models.Model):

    subject = models.ForeignKey(Subject,related_name='records')
    datetime = models.DateTimeField()
    intervention = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    weight = models.FloatField(null=True,blank=True)
    health = models.CharField(max_length=255)
    location = models.ForeignKey(Location,related_name='records')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['datetime']
        get_latest_by = "datetime"

    def __unicode__(self):
        return "%s: %s" % (self.datetime.ctime(),self.intervention)


