from configparser import ConfigParser
from pathlib import Path
from uuid import uuid4
from PySide6.QtCore import QProcessEnvironment


class MyConfig:
    def __init__(self, dev_mode: bool = True):
        config_dir = self._ensure_exists(
            Path.cwd().parent / "dev"
            if dev_mode
            else Path.home() / ".phystool"
        )

        self._data = ConfigParser()
        self._config_file = config_dir / "phystool.conf"
        if self._config_file.exists():
            self._data.read(self._config_file)
        else:
            if dev_mode:
                self._data['phystool'] = {"db": str(config_dir / "physdb_dev")}
            else:
                self._data['phystool'] = {"db": str(Path.home() / "physdb")}
            self._data['physnoob'] = {'editor': 'kile'}
            self._data['latex'] = {
                "auto": "physauto_dev",
                "tikz": "phystikz_dev",
            }
            self._data['git'] = {"theme": ""}
            with self._config_file.open('w') as out:
                self._data.write(out)

        self.PDB_DB_DIR = Path(self._data['phystool']['db']).expanduser()
        if not self.PDB_DB_DIR.exists():
            from shutil import copytree
            copytree(self.get_static_path() / "physdb_dev", self.PDB_DB_DIR)

        self.PDB_LATEX_AUX_DIR = self._ensure_exists(config_dir / "texaux")
        self.PDB_METADATA_DIR = self._ensure_exists(self.PDB_DB_DIR / "metadata")

        self.PDB_LOGFILE_PATH = config_dir / 'phystool.log'
        self.PDB_METADATA_PATH = self.PDB_METADATA_DIR / '0_metadata.pkl'
        self.PDB_TAGS_PATH = self.PDB_METADATA_DIR / '1_tags.json'
        self.PDB_EVALUATION_PATH = self.PDB_METADATA_DIR / '2_evaluations.json'
        self.PDB_LATEX_ENV = LaTeXEnv(self._ensure_exists(self.PDB_DB_DIR / "phystex"))
        # TODO: gather everything that concerns Latex config in one class
        self.PDB_LATEX_TEMPLATE = ""
        self.PDB_EDITOR_CMD: tuple[str, list[str]] = (self._data['physnoob']['editor'], [])
        if self.PDB_EDITOR_CMD[0] == "vim":
            self.PDB_EDITOR_CMD = ("rxvt-unicode", ["-e", "vim"])

        self.PDB_DELTA_THEME = self._data['git']['theme']
        self.PDB_BITBUCKET_API_KEY = "ATCTT3xFfGN0uBgFqH_ksSRPMDAtwwcykz_4uMw5nD6Q97bgYKAcRqn9L0DXte6e6QZ_0uSxfSTb0ovyt3RcPEi3mOKdDLIwrwjSFhlUsfxOx7EAbnS00uVa-OHTKVopBojiFThl3Ton7bsJJkjUdpEG2PXolDjCvI5i4DmoPTinj3HBdIqyEzs=A220AF8E"
        self.PDB_BITBUCKET_API_URL = "https://api.bitbucket.org/2.0/repositories/jdufour/phystool/src/master/CHANGELOG.md"

    def get_static_path(self) -> Path:
        if not hasattr(self, '_static_path'):
            from site import getsitepackages
            for site_package in getsitepackages():
                tmp = Path(site_package) / "phystool/static/"
                if tmp.exists():
                    self._static_path = tmp
                    return self._static_path
            raise FileNotFoundError("Static path not found")
        return self._static_path

    def _ensure_exists(self, path: Path) -> Path:
        if not path.exists():
            path.mkdir()
        return path

    def get_template(self, tex_file: Path) -> str:
        if not self.PDB_LATEX_TEMPLATE:
            self.PDB_LATEX_TEMPLATE = (
                f"\\documentclass{{{{{self._data['latex']['auto']}}}}}\n"
                f"\\PdbSetDBPath{{{{{self.PDB_DB_DIR}/}}}}\n"
                "\\begin{{document}}\n"
                "    \\PdbPrint{{{tex_file}}}\n"
                "\\end{{document}}"
            )

        return self.PDB_LATEX_TEMPLATE.format(tex_file=tex_file)

    def get_tikz_figure_documentclass(self) -> str:
        return self._data['latex']['tikz']

    def get_tex_file(self, uuid: str) -> Path:
        tex_file = (self.PDB_DB_DIR / uuid).with_suffix(".tex")
        if not tex_file.is_file():
            raise FileNotFoundError(tex_file)

        return tex_file

    def get_new_pdb_filename(self) -> Path:
        return (self.PDB_DB_DIR / str(uuid4())).with_suffix(".tex")

    def save_config(self, section: str, key: str, val: str) -> None:
        try:
            self._data[section][key] = val
        except KeyError:
            self._data.add_section(section)
            self._data[section][key] = val
        with self._config_file.open('w') as out:
            self._data.write(out)


class LaTeXEnv:
    def __init__(self, source: Path):
        self._env = {}
        self._source = source

    def __getitem__(
        self,
        qrocess: bool
    ) -> dict[str, str] | QProcessEnvironment:
        if not self._env:
            tmp = QProcessEnvironment.systemEnvironment()
            tmp.insert("TEXINPUTS", f":{self._source}:")
            self._env = {
                True: tmp,
                False: {
                    key: tmp.value(key)
                    for key in tmp.keys()
                }
            }
        return self._env[qrocess]
