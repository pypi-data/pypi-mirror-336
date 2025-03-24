from kyauthlib.jose import JsonWebKey
from kyauthlib.oidc.core import UserInfo


class OpenIDMixin:
    def fetch_jwk_set(self, force=False):
        metadata = self.load_server_metadata()
        jwk_set = metadata.get("jwks")
        if jwk_set and not force:
            return jwk_set

        uri = metadata.get("jwks_uri")
        if not uri:
            raise RuntimeError('Missing "jwks_uri" in metadata')

        with self.client_cls(**self.client_kwargs) as session:
            resp = session.request("GET", uri, withhold_token=True)
            resp.raise_for_status()
            jwk_set = resp.json()

        self.server_metadata["jwks"] = jwk_set
        return jwk_set

    def userinfo(self, **kwargs):
        """Fetch user info from ``userinfo_endpoint``."""
        metadata = self.load_server_metadata()
        resp = self.get(metadata["userinfo_endpoint"], **kwargs)
        resp.raise_for_status()
        data = resp.json()
        return UserInfo(data)

    def parse_id_token(self, token, nonce, claims_options=None, leeway=120):
        """Return an instance of UserInfo from token's ``id_token``."""
        if "id_token" not in token:
            return None

        metadata = self.load_server_metadata()

        import requests
        headers = {
            "Authorization": f"Bearer {token['access_token']}",
        }
        r = requests.get(metadata['userinfo_endpoint'] + f"?access_token={token['access_token']}", headers=headers, verify=False)
        if r and r.status_code == 200 and r.json() and r.json().get('data'):
            ui = r.json()["data"]
            ui['sub'] = ui['userId']
            ui['preferred_username'] = ui['username']
            # ui['nickname'] = ui['realName']
            return UserInfo(ui)
        else:
            return None

    def create_load_key(self):
        def load_key(header, _):
            jwk_set = JsonWebKey.import_key_set(self.fetch_jwk_set())
            try:
                return jwk_set.find_by_kid(header.get("kid"))
            except ValueError:
                # re-try with new jwk set
                jwk_set = JsonWebKey.import_key_set(self.fetch_jwk_set(force=True))
                return jwk_set.find_by_kid(header.get("kid"))

        return load_key
