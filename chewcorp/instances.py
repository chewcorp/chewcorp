import argparse
import json
import os
import sys
import time

from apiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools

class ComputeClient(object):
    def __init__(self, args):
        self.args = args
        self.storage_path = os.path.join(os.environ['HOME'], '.chewcorp')
        self.scope = 'https://www.googleapis.com/auth/compute.readonly'

    @property
    def client_secrets(self):
        secrets_path = os.path.join(self.storage_path, 'client_secrets.json')
        with open(secrets_path) as secrets_file:
            client_secret_data = json.load(secrets_file)
        return client_secret_data.get('installed')

    @property
    def credential_store(self):
        storage_path = os.path.join(self.storage_path, 'oauth_credentials')
        return Storage(storage_path)

    def client(self):
        http_client = httplib2.Http()
        credentials = self.credential_store.get()
        if not credentials or credentials.invalid:
            flow = client.OAuth2WebServerFlow(
                client_id=self.client_secrets['client_id'],
                client_secret=self.client_secrets['client_secret'],
                scope=self.scope,
                user_agent="chewcorp/0.1",
                redirect_url="urn:ietf:wg:oauth:2.0:oob",
            )
            tools.run_flow(flow, self.credential_store, self.args)
        # The older gdata api needs the oauth token to be converted
        self.credential_store.get().authorize(http_client)
        return http_client

    def service(self):
        return build('compute', 'v1', http=self.client())

    def list_instances(self, zones=None):
        if not zones:
            zones = self.list_zones()
        for zone in zones:
            instances = self.service().instances().list(
                project=self.args.project, zone=zone['description']).execute()
            if not instances.get('items'):
                continue
            for instance in instances['items']:
                yield instance

    def list_zones(self):
        zones = self.service().zones().list(
            project=self.args.project).execute()
        for zone in zones['items']:
            yield zone

def run():
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument(
        '--project', '-p', help='Project ID', type=str)
    parser.add_argument(
        '--zone', '-z', help='Zone ID', type=str, default=None)
    args = parser.parse_args()
    client = ComputeClient(args)
    instance_list = client.list_instances()
    for i in instance_list:
        print("%s: %s" % (i['name'], i['status']))


if __name__ == '__main__':
    run()
