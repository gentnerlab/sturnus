from django.db import models
from django_neo.models import Block

# Create your models here.


class Penetration(models.Model)
    pass
# associated w/ electrode
# has multiple sites
# belongs to subject
# has histology photos

class Depth(models.Model):
# M2M w/ block
# FK to Penetration
    pass