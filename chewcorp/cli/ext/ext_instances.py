from chewcorp import compute
from cement.core import controller, handler

class InstancesController(controller.CementBaseController):
    class Meta(object):
        label = 'instances'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Work with compute engine instances'

    @controller.expose(hide=True, aliases=['help'])
    def default(self):
        self.app.args.print_help()

    @controller.expose(help='List instances')
    def list(self):
        project = self.app.config.get('google', 'project')
        client = compute.ComputeClient(self.app.pargs, project)
        try:
            instances = client.list_instances()
        except (KeyError, TypeError) as err:
            self.app.log.info('No zone found: %r' % (err,))
        else:
            for instance in instances:
                print instance


def load(app=None):
    handler.register(InstancesController)
