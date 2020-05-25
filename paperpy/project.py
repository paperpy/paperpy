import os, json


class ProjectMetadata:
    """
        Description of a metadatum required to fill out a project proposal.
    """

    def __init__(self, name, label, help=None, choices=None, default=None):
        self.name = name
        self.label = label
        self.help = help
        self.choices = choices
        self.default = default
        self.value = None


class ProjectFile:
    """
        Description of a file that is created as part of a project proposal.
    """

    def __init__(self, template):
        self.template = template

    def create(self, proposal, path):
        with open(path, "w") as f:
            f.write(self.template)


_project_meta = [
    ProjectMetadata(
        name="document_format",
        label="Document Format",
        help="The format in which the document will be written",
        choices=["tex", "md", "docx"],
        default="tex",
    ),
    ProjectMetadata(
        name="publish_format",
        label="Publishing Format",
        help="The format in which the document will be published",
        choices=["pdf", "html", "md"],
        default="pdf",
    ),
]


_folder_structure = {
    ".paperpy": {"settings": ProjectFile(json.dumps({}))},
    "components": {},
    "figures": {},
    "tables": {},
    "documents": {},
}


class ProjectProposal:
    def __init__(self, dir, document_format="tex", publish_format="pdf"):
        self.dir = dir
        self.document_format = document_format
        self.publish_format = publish_format

    @classmethod
    def from_args(cls, args):
        kwargs = {"dir": args.directory}
        meta_kwargs = {m.name: args.__dict__[m.name] for m in _project_meta}
        kwargs.update(meta_kwargs)
        return cls(**kwargs)

    def create(self):
        folder = lambda *x: os.path.join(*x)

        def rec(f, s):
            if isinstance(s, ProjectFile):
                s.create(self, f)
            else:
                try:
                    os.mkdir(f)
                except FileExistsError:
                    raise FileExistsError(
                        "Could not create project: '{}' already exists".format(f)
                    ) from None
                for sf, ss in s.items():
                    rec(folder(f, sf), ss)

        rec(self.dir, _folder_structure)
