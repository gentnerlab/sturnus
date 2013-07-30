from django.db import models
from django_neo import Event, Lookup


class ProtocolType(Lookup):
    ''' what type of protocol is this? '''
    pass

class Protocol(models.Model):
    name = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)
    type = models.ForeignKey(ProtocolType,null=True,blank=True)
    
    def __unicode__(self):
        return self.name

class NaiveHierarchyManager(models.Manager):
    def get_roots(self):
        return self.get_query_set().filter(parent__isnull=True)

class NaiveHierarchy(models.Model):
    parent = models.ForeignKey('self', null=True)

    tree = NaiveHierarchyManager()

    def get_children(self):
        return self._default_manager.filter(parent=self)

    def get_descendants(self):
        descs = set(self.get_children())
        for node in list(descs):
            descs.update(node.get_descendants())
        return descs

    class Meta:
        abstract = True

class TrialSet(NaiveHierarchy):
    '''a container of trials and trial sets'''

    name = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)
    protocol = models.ForeignKey(Protocol,null=True,blank=True)

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

class ResponseTypes(Lookup):
    '''a class type

    e.g. Left, Right, Center, Probe
    '''
    pass

class Trial(Event):
    """ a single behavioral trial.
    holds meta information about the trial class & subject response

    """
    index = models.PositiveIntegerField()

    tr_type = models.ForeignKey(TrialTypes,null=True)
    tr_class = models.ForeignKey(TrialClassTypes,null=True)
    tr_resp = models.ForeignKey(ResponseTypes,null=True)

    reward_value = models.FloatField(null=True,blank=True)

    trial_sets = models.ManyToManyField(TrialSet,null=True)


    def __unicode__(self):
        return "%s" % (self.index)


class Stimulus(Event):
    ''' a stimulus presented in a behavioral trial'''
    pass

class RewardType(Lookup):
    ''' type of reward. e.g. food, water, juice, lights '''
    pass

class Reward(Event):
    ''' a reward. value can be negative '''
    value = models.FloatField(null=True,blank=True)
    pass


class Response(Event):
    ''' a subject's response '''
    pass
    
