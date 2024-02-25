"""
@author: Rajkumar Palanikumar (original work), Ibn Aleem (modified work)
@date: 15/01/2019 (original work), 25/02/2024 (modified work)
@description: PayPal environment class to store the client id, client secret, api url and web url of the environment to which the access token is to be sent to.
"""

import base64
from paypalhttp import Environment


class PayPalEnvironment(Environment):

    LIVE_API_URL = "https://api.paypal.com"
    LIVE_WEB_URL = "https://www.paypal.com"
    SANDBOX_API_URL = "https://api.sandbox.paypal.com"
    SANDBOX_WEB_URL = "https://www.sandbox.paypal.com"

    def __init__(self, client_id: str, client_secret: str, apiUrl: str, webUrl: str):
        super(PayPalEnvironment, self).__init__(apiUrl)
        self.client_id = client_id
        self.client_secret = client_secret
        self.web_url = webUrl

    def authorization_string(self):
        return f"Basic {base64.b64encode((self.client_id + ":" + self.client_secret).encode()).decode()}"


class SandboxEnvironment(PayPalEnvironment):
    def __init__(self, client_id: str, client_secret: str):
        super(SandboxEnvironment, self).__init__(client_id, client_secret, PayPalEnvironment.SANDBOX_API_URL, PayPalEnvironment.SANDBOX_WEB_URL)

class LiveEnvironment(PayPalEnvironment):

    def __init__(self, client_id: str, client_secret: str):
        super(LiveEnvironment, self).__init__(client_id,client_secret,PayPalEnvironment.LIVE_API_URL,PayPalEnvironment.LIVE_WEB_URL)