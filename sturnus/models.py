from django.db import models




# class Site(models.Model):
#     """ a single site/location of an electrode 
#     """
#     depth = models.IntegerField()
#     penetration = models.ForeignKey('Penetration')
#     blocks = models.ManyToManyField('Block')

#     def __unicode__(self):
#         return "%s,z%s" % (self.penetration, self.depth)

#
# class Population(models.Model):
#     name = models.CharField(64)
#     desc = models.CharField()

#     units = models.ManyToManyField('Unit')

#     def __unicode__(self):
#         return self.name

