from .baseresource import BaseResource


class LoginResource(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'login'
        attributes = {
            'sessionToken': 'session_token',
            'loginStatus': 'login_status',
        }


class KeepAliveResource(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'keep_alive'
        attributes = {
            'product': 'product',
            'status': 'status',
            'token': 'token',
            'error': 'error',
        }


class LogoutResource(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'logout'
        attributes = {
            'product': 'product',
            'status': 'status',
            'token': 'token',
            'error': 'error',
        }
