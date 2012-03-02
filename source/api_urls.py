from core.api import Api

from modules.projects.api import ProjectResource
from modules.profiles.api import ProfileResource
from modules.memberships.api import MembershipResource

v1_api = Api(api_name='1.0')
v1_api.register(ProjectResource())
v1_api.register(ProfileResource())
v1_api.register(MembershipResource())
