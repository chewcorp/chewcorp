'Work with CloudDNS'
import json
import os

from chewcorp import client

class DnsClient(client.DiscoveryClient):
    'Client for the CloudDNS API'
    def __init__(self, args, project):
        super(DnsClient, self).__init__()
        self.api = 'dns'
        self.args = args
        self.project = project
        self.storage_path = os.path.join(os.environ['HOME'], '.chewcorp')
        self.scope = 'https://www.googleapis.com/auth/ndev.clouddns.readwrite'
        self.version = 'v1'

    def list_zones(self):
        zones = self.service().managedZones()
        response = zones.list(project=self.project)
        print response
        #for zone in response['managedZones']:
        #   print json.dumps(zone)
