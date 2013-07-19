from django.db import models
from django_neo import RecordingChannel

class ElectrodeModel(models.Model):
    """ an electrode model 

    consider this a platonic electrode. it only exists in the pages of the neuronexus catalog
    """
    manufacturer = models.CharField(max_length=255)
    model_number = models.CharField(max_length=255)

    def __unicode__(self):
        return self.model_number

class SiteModel(models.Model):
    """ an electrode site model

    x & y & z coords are in microns when facing the electrode laying flat, from the lower left 

    this contains data common to every one of these pads across multiple electrodes
    """
    electrode_model = models.ForeignKey(ElectrodeModel)
    connector_chan = models.PositiveIntegerField(null=True)
    size = models.FloatField(null=True)
    size_units = models.CharField(max_length=255)
    x_coord = models.IntegerField(null=True)
    y_coord = models.IntegerField(null=True)
    z_coord = models.IntegerField(null=True)

    def __unicode__(self):
        return "{a:%s,x:%s,y:%s}" % (self.size, self.x_coord, self.y_coord)

class Electrode(models.Model):
    """ a single physical electrode 

    electrodes have real life analogs, with quirks and defects
    """
    serial_number = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.serial_number

class Site(models.Model):
    """ a single physical electrode site 

    one recording site on a real electrode
    """
    impedance = models.FloatField(null=True)
    electrode = models.ForeignKey(Electrode)
    electrode_pad_model = models.ForeignKey(ElectrodePadModel)
    notes =  models.TextField(blank=True)

    def __unicode__(self):
        return "%s:%s(%s)" % (self.electrode,self.electrode_pad_model.chan,self.impedance)

class ElectrodeRecordingChannel(RecordingChannel):
    ''' a recording channel '''
    chan = models.PositiveIntegerField()
    gain = models.FloatField(null=True)
    filter_high = models.FloatField(null=True)
    filter_low = models.FloatField(null=True)

    site = models.ForeignKey(Site)