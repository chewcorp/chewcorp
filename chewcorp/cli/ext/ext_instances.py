from chewcorp import instances
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

def load(app=None):
    handler.register(InstancesController)
