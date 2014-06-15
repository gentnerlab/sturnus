from django.db import models
from broab.models import Block, Unit, AnalogSignal
# from broab.models import Unit as BroabUnit
from broab.models import Lookup, BroabModel
from electrode.models import Electrode
from husbandry.models import Subject

# Create your models here.

class CoordinateSystem(Lookup):
    """ a coordinate system """
    pass

class Penetration(BroabModel):
    """ a single penetration of a neural probe 

    - foreign key to probe
    - has multiple depths
    - in a subject
    - coordinates & reference/system

    """

    HEMISPHERE_CHOICES = (
        ('R','Right'),
        ('L', 'Left'),
        )
    hemisphere = models.CharField(max_length=1,
                                  choices=HEMISPHERE_CHOICES)
    rostral = models.FloatField(default=0.0,help_text='negative is Caudal')
    lateral = models.FloatField(default=0.0)
    alpha_angle = models.FloatField(default=90)
    beta_angle = models.FloatField(default=0.0)
    rotation_angle = models.FloatField(default=0.0)
    depth_max = models.FloatField(null=True,blank=True)
    electrode = models.ForeignKey(Electrode)
    subject = models.ForeignKey(Subject)

    def __unicode__(self):
        return "%s, %s: %s(%s,%s)" % (self.subject,self.electrode,self.hemisphere,self.rostral,self.lateral)

class Location(BroabModel):
    """ a single location of an electrode """

    blocks = models.ManyToManyField(Block)
    penetration = models.ForeignKey(Penetration)
    depth = models.FloatField(default=0.0)

class SortQualityMethod(Lookup):
    """ a method to quantify sort quality """
    pass

class SortedUnit(Unit):
    """ a sorted unit """
    sort_quality = models.FloatField(null=True,blank=True)
    sort_quality_method = models.ForeignKey(SortQualityMethod,null=True,blank=True)
    multiunit = models.BooleanField()

    # def psth(self,label,bin_size=0.02,window=(0.0,1.0)):
    #     spike_trains = self.spike_trains.filter(event__label__name=label)

class Population(BroabModel):
    """ a population of recorded units """
    units = models.ManyToManyField(Unit)

# class LFP(AnalogSignal):
#     """ a local field potential

#     inherits from broab.models.AnalogSignal

#     """
#     pass
#     # additional features of a recorded LFP, such as...
#     # - cutoffs, filter type, etc
