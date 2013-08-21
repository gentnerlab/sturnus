from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from operant.models import ProtocolType, Protocol, TrialSet, TrialClass, TrialType, Trial
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
        
class ProtocolResource(BroabResource):


# extracellular


#