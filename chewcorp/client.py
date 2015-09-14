import json
import os

from apiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client.multistore_file import get_credential_storage
from oauth2client import tools

class DiscoveryClient(object):
    def __init__(self):
        self.api = None
        self.args = None
        self.scope = None
        self.storage_path = None
        self.user_agent = 'Chewcorp/0.1'
        self.version = None

    @property
    def client_secrets(self):
        secrets_path = os.path.join(self.storage_path, 'client_secrets.json')
        with open(secrets_path) as secrets_file:
            client_secret_data = json.load(secrets_file)
        return client_secret_data.get('installed')

    def credential_store(self):
        storage_path = os.path.join(self.storage_path, 'oauth_credentials')
        return get_credential_storage(
            storage_path,
            self.client_secrets['client_id'],
            self.user_agent,
            self.scope
        )

    def client(self):
        http_client = httplib2.Http()
        credential_store = self.credential_store()
        credentials = credential_store.get()
        if not credentials or credentials.invalid:
            flow = client.OAuth2WebServerFlow(
                client_id=self.client_secrets['client_id'],
                client_secret=self.client_secrets['client_secret'],
                scope=self.scope,
                user_agent=self.user_agent,
                redirect_url="urn:ietf:wg:oauth:2.0:oob",
            )
            tools.run_flow(flow, credential_store, self.args)
        credential_store.get().authorize(http_client)
        return http_client

    def service(self):
        return build(self.api, self.version, http=self.client())
