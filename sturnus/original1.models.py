from django.db import models

# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=100,
                            unique=True)

    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'X'
    SEX_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
        (UNKNOWN, 'unknown'),
        )
    sex = models.CharField(max_length=1,
                           choices=SEX_CHOICES,
                           default=UNKNOWN)

    def __unicode__(self):
        return self.name
