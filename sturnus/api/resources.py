from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from operant.models import ProtocolType, Protocol, Session, TrialClass, TrialType, Trial
from extracellular.models import CoordinateSystem, Penetration, Location, SortQualityMethod, Unit, Population
from broab.api.resources import BroabResource


# operant
class ProtocolTypeResource(ModelResource):

    class Meta():
        queryset = ProtocolType.objects.all()
        resource_name = 'protocol_type'
        filtering =  {
            'id': ALL,
            'name': ALL,
            'description': ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        
class ProtocolResource(ModelResource):
    class Meta():
        queryset = Protocol.objects.all()
        resource_name = 'protocol'
        filtering =  {
            'id': ALL,
            'name': ALL,
            'description': ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class SessionResource(ModelResource):
    class Meta():
        queryset = Session.objects.all()
        resource_name = 'session'
        filtering =  {
            'id': ALL,
            'name': ALL,
            'description': ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class TrialClassResource(ModelResource):
    class Meta():
        queryset = TrialClass.objects.all()
        resource_name = 'trial_class'
        filtering =  {
            'id': ALL,
            'name': ALL,
            'description': ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class TrialTypeResource(ModelResource):
    class Meta():
        queryset = TrialType.objects.all()
        resource_name = 'trial_type'
        filtering =  {
            'id': ALL,
            'name': ALL,
            'description': ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class TrialResource(ModelResource):
    class Meta():
        queryset = Trial.objects.all()
        resource_name = 'trial'
        filtering =  {
            'id': ALL,
            'name': ALL,
            'description': ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()