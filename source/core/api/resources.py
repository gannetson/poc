from tastypie.resources import Resource, ModelResource

from core.api.authentication import ChecksumAuthentication
from core.api.authorizations import ClientAuthorization
from core.api.paginator import Paginator
from core.api.serializers import HTMLSerializer
from core.api.throttle import BaseThrottle


class BaseResource(Resource):

    class Meta:
        serializer = HTMLSerializer()
        authentication = ChecksumAuthentication()
        authorization = ClientAuthorization()
        throttle = BaseThrottle(throttle_at=100, timeframe=3600)  # Throttle at 100 requests per hour
        paginator_class = Paginator


class BaseModelResource(ModelResource):
    class Meta(BaseResource.Meta):
        pass
