from django.db import models
from uuidfield import UUIDField
import base64


class Base64Field(models.TextField):
    """
    from http://djangosnippets.org/snippets/1669/
    """

    def contribute_to_class(self, cls, name):
        if self.db_column is None:
            self.db_column = name
        self.field_name = name + '_base64'
        super(Base64Field, self).contribute_to_class(cls, self.field_name)
        setattr(cls, name, property(self.get_data, self.set_data))

    def get_data(self, obj):
        return base64.decodestring(getattr(obj, self.field_name))

    def set_data(self, obj, data):
        setattr(obj, self.field_name, base64.encodestring(data))

    def db_type():
        return 'longtext'

class Subject(models.Model):
    """ one experimental subject """
    name = models.CharField(max_length=100,
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

class Block(models.Model):
    """ a single set of continuous trials. same as Dan's Epoch """
    title = models.SlugField(unique=True,max_length=255)
    desc = models.TextField(blank=True)
    subject = models.ForeignKey('Subject')
    datetime = models.DateTimeField()

    def __unicode__(self):
        return self.title

class Trial(models.Model):
    """ a single data structure to handle operant, acute, and chronic trials """
    block = models.ForeignKey('Block')
    tr_num = models.IntegerField()
    datetime = models.DateTimeField()

    class Meta:
        unique_together = (
            ('block','datetime'),
            ('block','tr_num'),
            )

    def __unicode__(self):
        return "%s:%s" % (self.block,self.tr_num)

class BehaviorTrial(Trial):
    TYPE_CHOICES = (
        ('norm', 'Normal'),
        ('crxn', 'Correction'),
        )
    tr_type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    RESP_CHOICES = [
        ('LT', 'Left'),
        ('RT', 'Right'),
        ('CT', 'Center'),
        ('NO', 'No response')
        ]
    CLASS_CHOICES = RESP_CHOICES + [('PR', 'Probe')]

    tr_class = models.CharField(max_length=2, choices=CLASS_CHOICES)
    response = models.CharField(max_length=2, choices=RESP_CHOICES)

    feed = models.BooleanField()
    timeout = models.BooleanField()
    cum_correct = models.IntegerField()
    cum_correct_thresh = models.IntegerField()

    def __unicode__(self):
        return "class: %s, resp: %s" % (self.tr_class, self.response)

class EventType(models.Model):
    """ Types of trial Events, e.g. peck """
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

class Event(models.Model):
    """ events that happen during a trial """
    trial = models.ForeignKey('Trial')
    event_type = models.ForeignKey('EventType')
    datetime = models.DateTimeField()
    desc = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return "%s @ %s" % (self.event_type,self.datetime)

class Stimulus(models.Model):
    """ meta info for stimulus epochs """
    file = models.FileField(upload_to='media/')

    class Meta:
        verbose_name_plural = "Stimuli"
    def __unicode__(self):
        return self.file.name

class EpochType(models.Model):
    """ types of trial epochs, e.g. stimulus, feed, timeout, flash, LED"""
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

class Epoch(models.Model):
    """ epochs that happen during a trial """

    trial = models.ForeignKey('Trial')
    epoch_type = models.ForeignKey('EpochType')
    start = models.DateTimeField()
    end = models.DateTimeField()
    desc = models.CharField(max_length=255,blank=True)

    def __unicode__(self):
        return "'%s':'%s'" % (self.start, self.end)

class ElectrodeModel(models.Model):
    """ an electrode model """
    manufacturer = models.CharField(max_length=255)
    model_number = models.CharField(max_length=255)

    def __unicode__(self):
        return self.model_number

class ElectrodePadModel(models.Model):
    """ an electrode site model, where x & y coords are in microns when facing the electrode laying flat """
    electrode_model = models.ForeignKey(ElectrodeModel)
    chan = models.CharField(max_length=3)
    size = models.IntegerField()
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()

    def __unicode__(self):
        return "{a:%s,x:%s,y:%s}" % (self.size, self.x_coord, self.y_coord)


class Electrode(models.Model):
    """ a single physical electrode """
    serial_number = models.CharField(max_length=255)

    def __unicode__(self):
        return self.serial_number

class ElectrodePad(models.Model):
    """ a single physical electrode site """
    impedance = models.FloatField(null=True)
    electrode = models.ForeignKey('Electrode')
    electrode_pad_model = models.ForeignKey('ElectrodePadModel')

    def __unicode__(self):
        return "%s:%s(%s)" % (self.electrode,self.electrode_pad_model.chan,self.impedance)

class Penetration(models.Model):
    """ a single electrode Penetration. coords relative to Y0"""
    HEMISPHERE_CHOICES = (
        ('R','right'),
        ('L', 'left'),
        )
    hemisphere = models.CharField(max_length=1,
                                  choices=HEMISPHERE_CHOICES)
    rostral = models.IntegerField(default=0)
    lateral = models.IntegerField(default=0)
    alpha_angle = models.FloatField(default=90)
    beta_angle = models.FloatField(default=0)
    rotation_angle = models.FloatField(default=0)
    depth_max = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s:r%s,l%s" % (self.hemisphere, self.rostral, self.lateral)

class Site(models.Model):
    """ a single site of an electrode """
    depth = models.IntegerField()
    penetration = models.ForeignKey('Penetration')
    blocks = models.ManyToManyField('Block')

    def __unicode__(self):
        return "%s,z%s" % (self.penetration, self.depth)

class Region(models.Model):
    """ a single brain region """
    abbrev = models.CharField(max_length=8)
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    is_part_of = models.ForeignKey('self',null=True,blank=True)

    def __unicode__(self):
        return self.abbrev

class RecordingChannel(models.Model):
    """ a single recording channel  """
    site = models.ForeignKey('Site')
    pad = models.ForeignKey('ElectrodePad')
    region = models.ForeignKey('Region', null=True, blank=True)

    class Meta:
            unique_together = (
            ('site','pad'),
            )

    def __unicode__(self):
        return self.pad.electrode_pad_model.chan


class Sort(models.Model):
    """ a single sort of a bunch of putative units """
    # image = models.ImageField(blank=True,null=True)
    trials = models.ManyToManyField('Trial')
    recording_channels = models.ManyToManyField('RecordingChannel',
                                                through='SortChannel')
    title = models.CharField(max_length=255,blank=True)

    def __unicode__(self):
        return self.title

class SortChannel(models.Model):
    """ a single channel from a sort """
    recording_channel = models.ForeignKey('RecordingChannel')
    sort = models.ForeignKey('Sort')
    threshold_upper = models.FloatField(default=2.5)
    threshold_lower = models.FloatField(default=-2.5)
    ORDER_CHOICES = (
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        )
    order = models.IntegerField(choices=ORDER_CHOICES)

    class Meta:
            unique_together = (
            ('sort','order'),
            )

    def __unicode__(self):
        return "%s:%s,%s" % (self.recording_channel, self.threshold_lower, self.threshold_upper)


class Isolation(models.Model):
    """a single isolation"""
    NUM_CHOICES = (
        ('single','Single Unit'),
        ('multi','Multiple Units'),
        )
    num_units = models.CharField(max_length=6,choices=NUM_CHOICES)
    CONFIDENCE_CHOICES = (
        (0,'0: noise'),
        (1,'1: bump'),
        (2,'2: very contaminated'),
        (3,'3: mostly separable'),
        (4,'4: very little contamination'),
        (5,'5: complete')
        )
    confidence = models.IntegerField(choices=CONFIDENCE_CHOICES)
    quality = models.FloatField(null=True, blank=True)
    sort = models.ForeignKey('Sort')
    primary_chan = models.ForeignKey('RecordingChannel') #TODO: add limit_choices_to=''

    def __unicode__(self):
        return "%s:%s(%s)" % (self.primary_chan,self.num_units,self.confidence)


# class AnalogSignal(models.Model):
#     """a single continuous analog signal """
#     chan = models.ForeignKey('RecordingChannel')
#     trial = models.ForeignKey('Trial')
#     time = models.DateTimeField()
#     sampling_rate = models.FloatField()
#     filtering = models.CharField()

#     def __unicode__(self):
#         return

class Unit(models.Model):
    label = models.SlugField()

    def __unicode__(self):
        return label

class SpikeTrain(models.Model):
    """a single spike train """
    isolation = models.ForeignKey('Isolation')
    unit = models.ForeignKey('Unit',null=True,blank=True)
    t_start = models.DateTimeField()
    t_stop = models.DateTimeField()

    def __unicode__(self):
        return "%s,%s" % (self.t_start,self.t_stop)

# class Spike(models.Model):
#     """ a single spike """
#     time = models.DateTimeField()

#     # waveforms = a 3D quantities array (channel_index, time)
#     sampling_rate = models.FloatField()
#     left_sweep = models.IntegerField()

# class Population(models.Model):
#     name = models.CharField(64)
#     desc = models.CharField()

#     units = models.ManyToManyField('Unit')

#     def __unicode__(self):
#         return self.name

# class TrialSet(models.Model):
#     name = models.CharField(64)
#     desc = models.CharField()

#     trials = models.ManyToManyField('Trial')

#     def __unicode__(self):
#         return self.name
