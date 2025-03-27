from logging.config import dictConfig

from phystool.config import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)


def phystool() -> None:
    from argparse import ArgumentParser
    from phystool.config import config
    from phystool.dmenuphys import DmenuPhys
    from phystool.helper import terminal_yes_no
    from phystool.latex import (
        PdfLatex,
        LatexLogParser,
        LogFileMessage
    )
    from phystool.metadata import Metadata
    from phystool.pdbfile import PDBFile
    from phystool.physgit import run_git_in_terminal
    from phystool.tags import Tags

    parser = ArgumentParser()

    parser.add_argument(
        "--search", help="Search in title",
        default=False, action='store_true', dest='search',
    )

    parser.add_argument(
        "--dmenu", help="Open file via dmenu",
        default=False, action='store_true', dest='dmenu',
    )

    parser.add_argument(
        "--list-tags", help="List all tags in Metadata",
        default=False, action='store_true', dest='list_tags',
    )

    parser.add_argument(
        "--add-tags", help="Add tags to given PDBFile",
        default=False, action='store_true', dest='add_tags',
    )

    parser.add_argument(
        "--remove-tags", help="Remove tags to given PDBFile",
        default=False, action='store_true', dest='remove_tags',
    )

    parser.add_argument(
        "--update", help="Update metadata by parsing PDB file",
        default=False, action='store_true', dest='update',
    )

    parser.add_argument(
        "--consolidate", help="Consolidate",
        default=False, action='store_true', dest='consolidate',
    )

    parser.add_argument(
        "--git", help="Commit modifications to git",
        default=False, action='store_true', dest='git',
    )

    parser.add_argument(
        "--get-new-pdb-filename", help="Returns new filename PDB",
        default=False, action='store_true', dest='get_new_pdb_filename',
    )

    parser.add_argument(
        "--remove", help="Remove PDB files",
        default=False, action='store_true', dest='remove',
    )

    parser.add_argument(
        "--reset", help="Reset PDB metadata (useful to change PDB_TYPE)",
        default=False, action='store_true', dest='reset',
    )

    parser.add_argument(
        "--compile", help="Compile .tex file to PDF",
        default=False, action='store_true', dest='compile'
    )

    parser.add_argument(
        "--tex-export-pdb-files", help="Print tex string multiple PdbFiles",
        nargs='*', default=None,  dest='tex_export_pdb_files',
    )

    parser.add_argument(
        "--pytex", help="Execute Python code",
        default=False, action='store_true', dest='pytex'
    )

    parser.add_argument(
        "--cat", help="Display in terminal",
        default=False, action='store_true', dest='cat'
    )

    parser.add_argument(
        "--pdb-file", help="PDB file selected",
        default="", dest='pdb_file', type=PDBFile.validate
    )

    parser.add_argument(
        "--query", help="Search in content",
        default=None, dest='query',
    )

    parser.add_argument(
        "--uuid-search", help="Search by uuid",
        default=None, dest='uuid_search',
    )

    parser.add_argument(
        "--tags", help="Selects tags",
        default="", dest='tags', type=Tags.validate
    )

    parser.add_argument(
        "--type", help="Selects 'exercise', 'qcm', 'theory' or 'tp'",
        default="", dest='type', type=Metadata.validate_type
    )

    parser.add_argument(
        "--zip", help="zip a PDB file with its dependencies",
        default=False, action='store_true', dest='zip'
    )

    parser.add_argument(
        "--texfile", help="Select a .tex file and set symlinks in .phystool",
        dest='texfile', type=PdfLatex.texfile_set_symlink
    )

    parser.add_argument(
        "--clean", help="Clean LaTeX auxiliary files",
        action='store_true', dest='clean'
    )

    parser.add_argument(
        "--output", help="Set .pdf name after LaTeX compilation",
        dest='output', type=PdfLatex.output
    )

    parser.add_argument(
        "--logtex", help="Analyse a LaTeX .log file",
        action='store_true', dest='logtex'
    )

    parser.add_argument(
        "--can-recompile", help="Alllow automatic recompilation",
        action='store_true', dest='can_recompile'
    )

    parser.add_argument(
        "--explicit-log", help="Display LaTeX raw error message",
        action='store_true', dest='explicit_log'
    )

    parser.add_argument(
        "--klass-list-current", help="List classes of the current year",
        action='store_true', dest='klass_list_current'
    )

    parser.add_argument(
        "--evaluation-list-current", help="List current evaluations",
        action='store_true', dest='evaluation_list_current'
    )

    parser.add_argument(
        "--evaluation-create-for-klass", help="Create new evaluation klass",
        dest='evaluation_create_for_klass'
    )

    parser.add_argument(
        "--evaluation-selected", help="Selected evaluation",
        dest='evaluation_selected'
    )

    parser.add_argument(
        "--evaluation-edit", help="Edit evaluation in extracted json file",
        action='store_true', dest='evaluation_edit'
    )

    parser.add_argument(
        "--evaluation-update", help="Update evaluation",
        action='store_true', dest='evaluation_update'
    )

    parser.add_argument(
        "--evaluation-search", help="Search evaluations using given PDBFile",
        action='store_true', dest='evaluation_search'
    )

    parser.add_argument(
        "--physnoob", help="Run physnoob",
        action='store_true', dest='physnoob'
    )

    args = parser.parse_args()

    if args.explicit_log:
        LogFileMessage.toggle_verbose_mode()

    if args.physnoob:
        return physnoob()

    if args.texfile:
        if args.logtex:
            llp = LatexLogParser(args.texfile)
            llp.process()
            llp.display()
            return

        lc = PdfLatex(args.texfile)
        if args.output:
            lc.full_compile(args.output, args.can_recompile)
        if args.clean:
            lc.clean([".aux", ".log", ".out", ".toc"])
        return

    if args.dmenu:
        dmenu = DmenuPhys()
        dmenu()
        return

    if args.tex_export_pdb_files:
        for uuid in args.tex_export_pdb_files:
            pdb_file = PDBFile.open(uuid)
            pdb_file.tex_export()
        return

    if args.get_new_pdb_filename:
        print(config.get_new_pdb_filename())
        return

    if args.pdb_file:
        pdb_file = args.pdb_file
        if args.compile:
            pdb_file.compile()
            return
        if args.list_tags:
            return pdb_file.tags.list_tags()
        if args.pytex:
            pdb_file.pytex()
            return
        if args.zip:
            return pdb_file.zip()
        if args.cat:
            return pdb_file.cat()

        metadata = Metadata()
        if args.remove:
            pdb_file.cat()
            if terminal_yes_no("Remove files?"):
                metadata.remove(pdb_file)
                metadata.save()
        elif args.reset:
            pdb_file.tex_file.with_suffix(".json").unlink(missing_ok=True)
            pdb_file = PDBFile.open(pdb_file.uuid)
            pdb_file.save()
            metadata.update(pdb_file)
            metadata.save()
        elif args.evaluation_search:
            metadata.evaluation_search(pdb_file.uuid)
        else:
            was_updated = False
            if args.tags:
                old_tags = pdb_file.tags.all()
                if args.add_tags:
                    pdb_file.tags += args.tags
                elif args.remove_tags:
                    pdb_file.tags -= args.tags
                was_updated = (old_tags != pdb_file.tags.all())
            elif args.update:
                was_updated = pdb_file.parse_texfile()

            if was_updated:
                pdb_file.save()
                metadata.update(pdb_file)
                metadata.save()
            print(pdb_file)
        return

    metadata = Metadata()
    if args.search:
        metadata.search(args.type, args.tags, args.query)
    elif args.uuid_search:
        metadata.uuid_search(args.uuid_search)
    elif args.consolidate:
        metadata.consolidate()
    elif args.klass_list_current:
        metadata.klass_list()
    elif args.evaluation_create_for_klass:
        metadata.evaluation_create_for_klass(args.evaluation_create_for_klass)
    elif args.evaluation_list_current:
        metadata.evaluation_list()
    elif args.evaluation_selected:
        if args.evaluation_edit:
            metadata.evaluation_edit(args.evaluation_selected)
        elif args.evaluation_update:
            metadata.evaluation_update(args.evaluation_selected)

    if args.git:
        run_git_in_terminal()

    if args.list_tags:
        Tags.list_valid_tags()
        return


def physnoob() -> None:
    try:
        from phystool.qt import PhysQt
        qt = PhysQt()
        qt.exec()
    except Exception as e:
        # If a tex file is missing from the DB (was manually removed), physnoob
        # will fail to start because it tries to display all pdb_files stored
        # in the db. It won't be able to sort the files and will raise an
        # exception. Here we just try to consolidate the metadata to start from
        # a clean DB
        from logging import getLogger
        from phystool.metadata import Metadata
        logger = getLogger(__name__)
        logger.exception(e)
        metadata = Metadata()
        metadata.consolidate()
