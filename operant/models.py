from django.db import models
from django.db.models.signals import post_init
from broab.models import Lookup, BroabModel
from broab.models import Event, EventLabel


class ProtocolType(Lookup):
    ''' what type of protocol is this? 

    e.g. Shape, Search, Random, Block

    '''
    pass

class Protocol(BroabModel):
    ''' a behavioral protocol 

    note: this is VERY likely to be experimenter & experiment specific

    '''
    type = models.ForeignKey(ProtocolType,null=True,blank=True)
    
    def __unicode__(self):
        return self.name

class TrialSet(BroabModel):
    '''container of trials

    '''

    protocol = models.ForeignKey(Protocol,null=True,blank=True)

    def __unicode__(self):
        return self.name

class TrialType(Lookup):
    ''' a type of trial 

    e.g. Normal, Correction, Catch
    '''
    pass

class TrialClass(Lookup):
    '''a class type

    e.g. Left, Right, Center, Probe, GO, NOGO
    '''
    pass

    class Meta(Lookup.Meta):
        verbose_name = "trial class"
        verbose_name_plural = "trial classes"

class Trial(Event):
    """ a single behavioral trial

    holds meta information about the trial class & subject response

    """
    index = models.PositiveIntegerField(null=True)

    tr_type = models.ForeignKey(TrialType,null=True)
    tr_class = models.ForeignKey(TrialClass,null=True,related_name='trial_set_as_class')
    stimulus = models.CharField(max_length=255,blank=True)

    response = models.ForeignKey(TrialClass,null=True,related_name='trial_set_as_response')

    def correct(self):
        return (self.tr_class == self.response)
    correct.boolean = True
    
    reinforced = models.NullBooleanField()

    trial_set = models.ForeignKey(TrialSet)

   


    def __unicode__(self):
        return "%s" % (self.index)

    def save(self, *args, **kwargs):
        event_label, created = EventLabel.objects.get_or_create(name='trial') 
        self.label = event_label
        super(Trial, self).save(*args, **kwargs)

# def set_trial_label(**kwargs):
#    trial = kwargs.get('instance')
#    trial.label = EventLabel.objects.get_or_create(name='trial')

# post_save.connect(set_trial_label, Trial)
    
