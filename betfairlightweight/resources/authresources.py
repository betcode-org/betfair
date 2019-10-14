from .baseresource import BaseResource


class LoginResource(BaseResource):
    def __init__(self, **kwargs):
        super(LoginResource, self).__init__(**kwargs)
        self.session_token = kwargs.get("sessionToken")
        self.login_status = kwargs.get("loginStatus")


class KeepAliveResource(BaseResource):
    def __init__(self, **kwargs):
        super(KeepAliveResource, self).__init__(**kwargs)
        self.product = kwargs.get("sessionToken")
        self.status = kwargs.get("status")
        self.token = kwargs.get("token")
        self.error = kwargs.get("error")


class LogoutResource(BaseResource):
    def __init__(self, **kwargs):
        super(LogoutResource, self).__init__(**kwargs)
        self.product = kwargs.get("product")
        self.status = kwargs.get("status")
        self.token = kwargs.get("token")
        self.error = kwargs.get("error")
