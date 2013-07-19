from django.db import models
from django_neo import Event, Lookup

# Create your models here.

class Subject(models.Model):
    """ an experimental subject 

    subjects can have the following:
    - name [CharField] (unique)
    - sex [CharField]

    for consideration:
    - origin (a location, e.g. LAX)
    - acquisiton date
    - age at acquisition

    """
    name = models.CharField(max_length=255,
                            unique=True)
    SEX_CHOICES = (
        ('M', 'male'),
        ('F', 'female'),
        ('U', 'unknown'),
        )
    sex = models.CharField(max_length=1,
                           choices=SEX_CHOICES,
                           default='U')

    def __unicode__(self):
        return self.name


class TrialSet(models.Model):
    '''a container of trials and trial sets'''

    name = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)

    trial_set = models.ForeignKey('TrialSet',null=True)

    def __unicode__(self):
        return self.name

class TrialType(Lookup):
    ''' a type of trial 

    e.g. Normal, Correction, Catch
    '''
    pass

class TrialClassTypes(Lookup):
    '''a class type

    e.g. Left, Right, Center, Probe
    '''
    pass

class Trial(models.Model):
    """ a single behavioral trial.

    """
    index = models.PositiveIntegerField()

    tr_type = models.ForeignKey(TrialTypes)
    tr_class = models.ForeignKey(TrialClassTypes)
    tr_resp = models.ForeignKey(TrialClassTypes)

    reward_value = models.FloatField()

    trial_sets = models.ManyToManyField(TrialSet)


    def __unicode__(self):
        return "class: %s, resp: %s" % (self.tr_class, self.response)


class Stimulus(Event):
    ''' a stimulus presented in a behavioral trial'''
    pass

