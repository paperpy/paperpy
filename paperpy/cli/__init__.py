from .plugins import discover
import argparse

def _construct_parser():
    """
        Construct the fully populated argument parser.
    """
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--version",action="store_true",help="Show version")
    parser.set_defaults(handler=base_command)
    # Subparsers
    subparsers = parser.add_subparsers(
        title="Actions",
        description="All available actions to perform.",
        dest="action",
    )
    # Collect the `action` plugins, they need to return an object that implements the
    # paperpy.interfaces.Action interface.
    for plugin in discover("action"):
        # Create the subparser with the plugin defined arguments and name.
        plugin_parser = subparsers.add_parser(plugin.__name__, **plugin.get_parser_args())
        # Fill the parser object with its arguments etc.
        plugin.fill_parser(plugin_parser)
        # Set all arguments that are 'global' => They should work in any position in the
        # command. Eg the following 2 commands should be equivalent:
        # paperpy --config=A lint
        # paperpy lint --config=A
        _apply_global_arguments(plugin_parser)
        # Set the `handler` argument to the command handler
        plugin_parser.set_defaults(handler=plugin.handle_command)

    return parser

# A list of tuples of args & kwargs to be given to the `parser.add_argument` function.
_global_arguments = [
    # ([], {})
]

def _apply_global_arguments(parser):
    """
        Apply the global arguments to a parser.
    """
    for arg in _global_arguments:
        parser.add_argument(*arg[0], **arg[1])

def handle_command():
    """
        Handle CLI command. Collect all available actions, use
        ``argparse`` to parse the arguments and then execute the action's handler.
    """
    # Get the fully populated argparser
    parser = _construct_parser()
    # Parse the arguments
    args = parser.parse_args()
    # Execute the handler. Every subparser has handler so either it is set or the
    # ArgumentParser informs the user that the given command does not exist and this code
    # isn't reached.
    args.handler(args)

def base_command(args):
    """
        The handler for the ``paperpy`` command withot any specified action.
    """
    if args.version:
        from .. import __version__
        print(__version__)
