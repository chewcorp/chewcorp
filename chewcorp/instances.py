import os

from chewcorp import client

class ComputeClient(client.DiscoveryClient):
    def __init__(self, args):
        super(ComputeClient).__init__()
        self.args = args
        self.storage_path = os.path.join(os.environ['HOME'], '.chewcorp')
        self.scope = 'https://www.googleapis.com/auth/compute.readonly'
        self.api = 'compute'
        self.version = 'v1'

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
