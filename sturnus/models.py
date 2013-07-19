from django.db import models

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


class Penetration(models.Model):
    """ a single electrode Penetration. coords relative to Y0


    consider: make zero coordinate a field in the penetration
    """
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

# class Site(models.Model):
#     """ a single site/location of an electrode 
#     """
#     depth = models.IntegerField()
#     penetration = models.ForeignKey('Penetration')
#     blocks = models.ManyToManyField('Block')

#     def __unicode__(self):
#         return "%s,z%s" % (self.penetration, self.depth)

# class Region(models.Model):
#     """ a single brain region """
#     abbrev = models.CharField(max_length=8)
#     name = models.CharField(max_length=255)
#     url = models.URLField(blank=True)
#     is_part_of = models.ForeignKey('self',null=True,blank=True)

#     def __unicode__(self):
#         return self.abbrev

#
# class Population(models.Model):
#     name = models.CharField(64)
#     desc = models.CharField()

#     units = models.ManyToManyField('Unit')

#     def __unicode__(self):
#         return self.name

