from tastypie.resources import ModelResource
from sturnus.models import *

class SubjectResource(ModelResource):
    class Meta:
        queryset = Subject.objects.all()