import json
import urllib.parse

from oauthenticator.oauth2 import OAuthenticator, OAuthLogoutHandler
from tornado import httpclient
from traitlets import Bool, Unicode


class EODHLogoutHandler(OAuthLogoutHandler):
    """Log a user out by clearing both their JupyterHub login cookie and SSO cookie."""

    async def get(self):
        self.log.info("EODH Logout")
        if self.authenticator.enable_logout:
            await self.default_handle_logout()
            await self.handle_logout()

            redirect_url = self.authenticator.oauth_logout_url
            if self.authenticator.oauth_logout_redirect_uri:
                redirect_url += (
                    f"?redirect_uri={self.authenticator.oauth_logout_redirect_uri}"
                )

            self.redirect(redirect_url)
        else:
            await super().get()


class EODHAuthenticator(OAuthenticator):
    enable_logout = Bool(False, config=True)
    oauth_logout_url = Unicode(config=True)
    oauth_logout_redirect_uri = Unicode(config=True)

    logout_handler = EODHLogoutHandler

    def build_auth_state_dict(self, token_info, user_info):
        """
        Add workspaces claim to auth_state if present in user_info.
        """
        auth_state = super().build_auth_state_dict(token_info, user_info)
        if "workspaces" in user_info:
            auth_state["workspaces"] = user_info["workspaces"]
            self.log.info(
                "Workspaces added to auth_state: %s", auth_state["workspaces"]
            )
        else:
            self.log.warning("No workspaces claim in user token info")
        return auth_state

    async def exchange_token(self, subject_token: str, scope: list[str]) -> str:
        """
        Exchange the subject_token for new credentials with different scope.
        """
        self.log.info("Exchanging user token for workspace token...")
        http = httpclient.AsyncHTTPClient()
        headers = self.build_token_info_request_headers()
        body = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "subject_token": subject_token,
            "scope": " ".join(scope),
        }
        self.log.info("Exchanging token with headers: %s", headers)
        self.log.info("Exchanging token with body: %s", body)
        response = await http.fetch(
            self.authorize_url,
            method="POST",
            headers=headers,
            body=urllib.parse.urlencode(body).encode("utf8"),
        )
        response.rethrow()
        self.log.info("Token exchange successful")
        return json.loads(response.body.decode("utf8"))
