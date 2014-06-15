from django.db import models
from django.db.models.signals import post_init
from broab.models import Lookup, BroabModel
from broab.models import Event, EventLabel
from husbandry.models import Subject
# from pyoperant import behavior


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

class Session(BroabModel):
    '''container of trials

    '''
    subject = models.ForeignKey(Subject)
    index = models.PositiveIntegerField(null=True,blank=True)
    protocol = models.ForeignKey(Protocol,null=True,blank=True)
    accuracy = models.FloatField(null=True,blank=True,help_text='Only normal trials. Ignores probes and non-responses. Updates on save.')
    d_prime = models.FloatField(null=True,blank=True,help_text='Only normal trials. Ignores probes and non-responses. Updates on save.')

    # @property
    # def confusion_matrix(self):
    #     classes = []
    #     responses = []
    #     trial_set = self.trials.filter(tr_type__name__iexact='normal')\
    #         .exclude(tr_class__name__iexact='probe')\
    #         .exclude(tr_class__name__iexact='no response')
    #     for trial in trial_set:
    #         classes.append(trial.tr_class.id)
    #         responses.append(trial.response.id)
    #     return behavior.ConfusionMatrix(responses,classes)

    # def calc(self):
    #     confusion = self.confusion_matrix
    #     self.accuracy = confusion.acc()
    #     self.d_prime = confusion.dprime()

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
    session = models.ForeignKey(Session,related_name='trials')
    index = models.PositiveIntegerField(null=True,blank=True)

    tr_type = models.ForeignKey(TrialType,null=True)
    tr_class = models.ForeignKey(TrialClass,null=True,related_name='trials_as_class')
    stimulus = models.CharField(max_length=255,blank=True)
    response = models.ForeignKey(TrialClass,null=True,related_name='trials_as_response')
    correct = models.NullBooleanField()
    reinforced = models.NullBooleanField()
    reaction_time = models.FloatField(null=True,blank=True)

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
    
