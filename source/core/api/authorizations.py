from tastypie.authorization import Authorization

from .models import Client, Resource


class ClientAuthorization(Authorization):

    def _get_client(self, request):
        """Return the client based on the request (api_key)
        We can assume it's present as we already authorized the client by the time we get here
        """
        return request.api_client

    def _get_or_create_resource(self, resource_identifier):
        """We get or create a resource
        Easy way to automatically get the resources in the system
        """
        obj, created = Resource.objects.get_or_create(resource_identifier=resource_identifier)
        return obj

    def is_authorized(self, request, object=None):
        """Note that object is never passed"""
        client = self._get_client(request)
        resource_identifier = self.resource_meta.resource_name
        resource = self._get_or_create_resource(resource_identifier)
        if resource.clients.filter(pk=client.pk).exists():
            return client is not None
        return False

    def apply_limits(self, request, object_list):
        return object_list
