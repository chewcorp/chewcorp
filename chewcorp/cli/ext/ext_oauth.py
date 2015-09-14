import argparse

from cement.core import hook
from oauth2client import tools

def load_google_args(app):
    if not isinstance(app.args, argparse.ArgumentParser):
        raise TypeError('Cannot add arguments to non argparse parser %r' % (
            app.args))
    app.args._add_container_actions(tools.argparser)
    app.args.set_defaults(noauth_local_webserver=True)


def load(app=None):
    hook.register('pre_argument_parsing', load_google_args)
