from tastypie.resources import ModelResource
from sturnus.models import Subject


class SubjectResource(ModelResource):
    class Meta:
        queryset = Subject.objects.all()
