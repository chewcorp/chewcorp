from cement.core import controller, handler

from chewcorp import dns

class DnsController(controller.CementBaseController):
    class Meta(object):
        label = 'dns'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Work with clouddns'

    @controller.expose(hide=True, aliases=['help'])
    def default(self):
        self.app.args.print_help()

    @controller.expose(help='List zones')
    def list(self):
        project = self.app.config.get('google', 'project')
        dnsclient = dns.DnsClient(self.app.pargs, project)
        try:
            zones = dnsclient.list_zones()['managedZones']
        except (KeyError, TypeError) as err:
            self.app.log.info('No managed zones found: %r' % (err,))
        else:
            for zone in zones:
                print zone['dnsName']


class GetZone(controller.CementBaseController):
    class Meta(object):
        label = 'get_zone'
        stacked_on = 'dns'
        stacked_type = 'nested'
        aliases = ['get']
        aliases_only = True
        help = 'Fetch zone details'
        arguments = [
            (['zone'], {
                'help': 'Zone to fetch',
            })
        ]

    @controller.expose(hide=True)
    def default(self):
        project = self.app.config.get('google', 'project')
        dnsclient = dns.DnsClient(self.app.pargs, project)
        try:
            zone = dnsclient.get_zone(self.app.pargs.zone)
        except (KeyError, TypeError) as err:
            self.app.log.info('No zone found: %r' % (err,))
        else:
            print zone



def load(app=None):
    handler.register(DnsController)
    handler.register(GetZone)
