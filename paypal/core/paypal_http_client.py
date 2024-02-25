"""
@author: Rajkumar Palanikumar (original work), Ibn Aleem (modified work)
@date: 15/01/2019 (original work), 25/02/2024 (modified work)
@description: PayPal HTTP client class to make HTTP requests to the PayPal API. It also handles the access token and refresh token.
"""

import platform
from paypalhttp import HttpClient
from core import AccessTokenRequest, AccessToken, RefreshTokenRequest

class PayPalHttpClient(HttpClient):
    def __init__(self, environment, refresh_token=None):
        HttpClient.__init__(self, environment)
        self._refresh_token = refresh_token
        self._access_token = None
        self.environment = environment
        self.add_injector(injector=self)

    def __call__(self, request):
        request.headers["sdk_name"] = "Payouts SDK"
        request.headers["sdk_version"] = "1.0.1"
        request.headers["sdk_tech_stack"] = f"Python {platform.python_version()}"
        request.headers["api_integration_type"] = "Paypal Payouts SDK"

        if "Accept-Encoding" not in request.headers:
            request.headers["Accept-Encoding"] = "gzip"

        if (
            "Authorization" not in request.headers
            and not isinstance(request, AccessTokenRequest)
            and not isinstance(request, RefreshTokenRequest)
        ):
            if not self._access_token or self._access_token.is_expired():
                accesstokenresult = self.execute(
                    AccessTokenRequest(self.environment, self._refresh_token)
                ).result
                self._access_token = AccessToken(
                    access_token=accesstokenresult.access_token,
                    expires_in=accesstokenresult.expires_in,
                    token_type=accesstokenresult.token_type,
                )

            request.headers["Authorization"] = self._access_token.authorization_string()
