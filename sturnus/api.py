from tastypie.resources import ModelResource
from sturnus.models import *

class SubjectResource(ModelResource):
    class Meta:
        queryset = Subject.objects.all()

class BlockResource(ModelResource):
    class Meta:
        queryset = Block.objects.all()

class TrialResource(ModelResource):
    class Meta:
        queryset = Trial.objects.all()

class BehaviorTrialResource(ModelResource):
    class Meta:
        queryset = BehaviorTrial.objects.all()

class EventTypeResource(ModelResource):
    class Meta:
        queryset = EventType.objects.all()

class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
