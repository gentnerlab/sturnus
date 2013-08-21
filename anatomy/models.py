from django.db import models

# class Region(models.Model):
#     """ a single brain region """
#     abbrev = models.CharField(max_length=8)
#     name = models.CharField(max_length=255)
#     url = models.URLField(blank=True)
#     is_part_of = models.ForeignKey('self',null=True,blank=True,related_name='parts')
#     projects_to = models.ManyToManyField('self',null=True,through='Projection',related_name='gets_projections_from')

#     def __unicode__(self):
#         return self.abbrev

class Projection(models.Model):
    """ a single projection between regions """
    PMIDs = models.TextField(blank=True)
    origin = models.ForeignKey(Region)
    termination = models.ForeignKey(Region)

class Slice(models.Model):
    pass

class Image(models.Model):
    slice = models.ForeignKey(Slice)
