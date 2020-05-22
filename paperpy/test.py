from .interfaces import Action

class eyo(Action):
    def get_parser_args(self):
        return dict(help="Just a test")

    def fill_parser(self, parser):
        pass

    def handle_command(self, args):
        print("Weeeeee", args)
