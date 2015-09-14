from cement.core import controller, handler

from chewcorp import dns

class DnsController(controller.CementBaseController):
    class Meta(object):
        label = 'dns'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Work with clouddns'
        arguments = [
            (['--project', '-p'], {
                    'help': 'Select the projectid to work with',
            }),
        ]

    @controller.expose(hide=True, aliases=['help'])
    def default(self):
        self.app.args.print_help()

    @controller.expose(help='List zones')
    def list(self):
        dnsclient = dns.DnsClient(self.app.pargs, self.app.pargs.project)
        for zone in dnsclient.list_zones():
            print zone

def load(app=None):
    handler.register(DnsController)
