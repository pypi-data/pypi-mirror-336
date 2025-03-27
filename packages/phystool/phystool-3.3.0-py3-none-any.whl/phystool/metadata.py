import json
import pickle

from logging import getLogger
from pathlib import Path
from typing import Iterator
from uuid import uuid4

from phystool.helper import (
    greptex,
    lower_ascii,
    Klass,
    Evaluation,
    progress_bar
)
from phystool.config import config
from phystool.pdbfile import (
    Exercise,
    Figure,
    PDBFile,
    VALID_TYPES,
)
from phystool.tags import Tags

logger = getLogger(__name__)


class Metadata:
    @classmethod
    def validate_type(cls, list_of_types: str) -> list[str]:
        if not list_of_types:
            return []

        out = []
        for file_type in list_of_types.split(','):
            if file_type not in VALID_TYPES:
                raise ValueError
            out.append(file_type)

        return out

    def __init__(self) -> None:
        if not config.PDB_METADATA_PATH.exists():
            logger.debug("Create metadata file")
            self._pdb_data: dict[str, PDBFile] = {}
            exercises_in_evaluation = []
            for tex_file in config.PDB_DB_DIR.glob('*.tex'):
                try:
                    pdb_file = PDBFile.open(tex_file.stem)
                    self._pdb_data[pdb_file.uuid] = pdb_file
                    if pdb_file.PDB_TYPE == Exercise.PDB_TYPE:
                        exercises_in_evaluation += [
                            (uuid, pdb_file.uuid)
                            for uuid in pdb_file.evaluations
                        ]
                except ValueError as e:
                    logger.error(e)
                    logger.error("Ignoring file")

            if config.PDB_EVALUATION_PATH.exists():
                with config.PDB_EVALUATION_PATH.open() as jsin:
                    data = json.load(jsin)
                    self._klasses = {
                        uuid: Klass(uuid=uuid, **klass)
                        for uuid, klass in data['klasses'].items()
                    }
                    self._evaluations = {
                        uuid: Evaluation(uuid=uuid, **evaluation)
                        for uuid, evaluation in data['evaluations'].items()
                    }
            else:
                self._klasses = {}
                self._evaluations = {}

            self.save()

    def __new__(self, load=True):
        """
        unpickle if config.PDB_METADATA_PATH exists, otherwise creates it with
        __init__
        """
        if load:
            if config.PDB_METADATA_PATH.exists():
                with config.PDB_METADATA_PATH.open('rb') as pkl:
                    logger.debug("Loading metadata.")
                    try:
                        return pickle.load(pkl)
                    except Exception:
                        pass
                config.PDB_METADATA_PATH.unlink()
            logger.error(f"Loading {config.PDB_METADATA_PATH} failed, create")
        return super().__new__(self)

    def __getnewargs__(self):
        """
        Called by pickle to override default 'load' argument. Somehow, it seems
        to be called when saving, not loading, despite what I understand from
        the docs.
        """
        return False,

    def get_klass(self, name: str, year: int) -> Klass:
        for k in self._klasses.values():
            if k.name == name and k.year == year:
                return k
        raise ValueError

    def klass_list(self, current: bool = True) -> None:
        for uuid, klass in self._klasses.items():
            if not current or klass.is_current():
                print(f"{uuid}: {klass.name}")

    def klass_display(self, klass_uuid: str) -> None:
        klass = self._klasses[klass_uuid]
        print(klass)
        for uuid in klass.evaluations:
            self.evaluation_display(uuid)

    def evaluation_list(self, current: bool = True) -> None:
        for klass in self._klasses.values():
            if not current or klass.is_current():
                for uuid in klass.evaluations:
                    print(f"{uuid}: {klass.name:<5} {self._evaluations[uuid]}")

    def evaluation_create_for_klass(self, klass_uuid: str) -> str:
        uuid = str(uuid4())
        evaluation = Evaluation(
            uuid=uuid,
            klass_uuid=klass_uuid,
        )
        self._evaluations[uuid] = evaluation
        self._klasses[klass_uuid].evaluations.append(uuid)
        self._save_evaluation(evaluation)
        return uuid

    def evaluation_edit(self, evaluation_uuid: str) -> None:
        fname = Path(f"/tmp/{evaluation_uuid}.json")
        with fname.open('w') as jsout:
            json.dump(
                self._evaluations[evaluation_uuid].to_dict(),
                jsout,
                indent=4,
                ensure_ascii=False
            )

    def evaluation_update(self, evaluation_uuid: str) -> None:
        try:
            evaluation = self._evaluations[evaluation_uuid]
        except KeyError:
            logger.error(f"Evaluation with {evaluation_uuid} not found")
            return

        fname = Path(f"/tmp/{evaluation_uuid}.json")
        with fname.open() as jsin:
            data = json.load(jsin)

        to_del, to_add = evaluation.update(data)
        for uuid in to_del:
            self._pdb_data[uuid].evaluations.remove(evaluation_uuid)
            self._pdb_data[uuid].save()
        for uuid in to_add:
            self._pdb_data[uuid].evaluations.add(evaluation_uuid)
            self._pdb_data[uuid].save()

        self._save_evaluation(evaluation)

    def evaluation_display(self, evaluation_uuid: str) -> None:
        evaluation = self._evaluations[evaluation_uuid]
        print(f"{evaluation} -> {self._klasses[evaluation.klass_uuid]}")
        for uuid in evaluation.exercises:
            print(f"\t{self._pdb_data[uuid]}")

    def evaluation_search(self, uuid: str) -> None:
        pdb_file = self._pdb_data[uuid]
        if pdb_file.PDB_TYPE == Exercise.PDB_TYPE:
            for evaluation_uuid in pdb_file.evaluations:
                self.evaluation_display(evaluation_uuid)

    def _save_evaluation(self, evaluation: Evaluation) -> None:
        with config.PDB_EVALUATION_PATH.open() as jsin:
            data = json.load(jsin)

        data['evaluations'][evaluation.uuid] = evaluation.to_dict()
        data['evaluations'] = {
            uuid: evaluation
            for uuid, evaluation in sorted(
                data['evaluations'].items(),
                key=lambda x: self._evaluations[x[0]]
            )
        }
        data['klasses'][evaluation.klass_uuid]['evaluations'].append(evaluation.uuid)

        for klass in data['klasses'].values():
            klass['evaluations'] = sorted(
                set(klass['evaluations']),
                key=lambda x: self._evaluations[x]
            )

        with config.PDB_EVALUATION_PATH.open('w') as jsout:
            json.dump(data, jsout, indent=4, ensure_ascii=False)
        self.save()

    def _get_list(
        self,
        file_types: list[str],
        tags: Tags = Tags(),
    ) -> Iterator[PDBFile]:
        for pdb_file in self._pdb_data.values():
            if pdb_file.PDB_TYPE in file_types:
                if pdb_file.tags.include(tags):
                    yield pdb_file

    def _search(
        self,
        list_iterator: Iterator[PDBFile],
        query: str
    ) -> Iterator[PDBFile]:
        if matched_uuids := greptex(query, config.PDB_DB_DIR, False):
            for pdb_file in list_iterator:
                if pdb_file.uuid in matched_uuids:
                    yield pdb_file

    def search(
        self,
        file_types: list[str],
        tags: Tags,
        query: str
    ) -> None:
        list_iterator = self._get_list(file_types=file_types, tags=tags)
        if query:
            list_iterator = self._search(list_iterator, query)
        for pdb_file in list_iterator:
            print(f"{pdb_file.uuid}:{pdb_file.title:<43}{pdb_file.tags.cursus:>23}")

    def uuid_search(self, bit: str) -> None:
        for uuid, pdb_file in self._pdb_data.items():
            if bit in uuid:
                print(f"{uuid}:{pdb_file.title}")

    def dmenu_dict(self, file_types: list[str]) -> dict[str, str]:
        return {
            pdb_file.to_dmenu(): pdb_file.uuid
            for pdb_file in sorted(
                self._get_list(file_types=file_types),
                reverse=True
            )
        }

    def update(self, pdb_file: PDBFile) -> None:
        try:
            old_title = self._pdb_data[pdb_file.uuid].title
        except KeyError:
            old_title = ""

        self._pdb_data[pdb_file.uuid] = pdb_file
        if pdb_file.title != old_title:
            # sort when a new pdb_file is added or when title changes
            self._pdb_data = dict(
                sorted(
                    self._pdb_data.items(),
                    key=lambda x: (
                        lower_ascii(x[1].title),
                        x[1].PDB_TYPE,
                        x[0]  # uuid
                    )
                )
            )

    def remove(self, pdb_file: PDBFile) -> None:
        try:
            del self._pdb_data[pdb_file.uuid]
        except KeyError:
            logger.error(f"Failed to remove {pdb_file} from metadata")
            return

        for pdb in config.PDB_DB_DIR.glob(pdb_file.uuid + '*'):
            logger.info(f"Removing {pdb}")
            pdb.unlink()

    def consolidate(self) -> None:
        _message = ""
        for i, n, message in self.consolidate_progress():
            if _message != message:
                _message = message
                print()
            progress_bar(n, i, 20, f"{message:<30} |")
        print()

    def consolidate_progress(self) -> Iterator[tuple[int, int, str]]:
        pdb_files: dict[str, list[PDBFile]] = {
            pdb_type: []
            for pdb_type in VALID_TYPES
        }
        figure_used_by: dict[str, set[str]] = {}
        tex_files = list(config.PDB_DB_DIR.glob('*.tex'))
        message = "Parsing"
        i = 0
        n = len(tex_files)
        for tex_file in tex_files:
            i += 1
            yield i, n, message
            pdb_file = PDBFile.open(tex_file.stem)
            if not pdb_file.parse_texfile():
                logger.warning(f"Failed to parse {pdb_file} ({pdb_file.uuid})")
                continue
            if not pdb_file.tags:
                logger.warning(f"{pdb_file} ({pdb_file.uuid}) is untagged")

            self.update(pdb_file)
            pdb_file.save()
            pdb_files[pdb_file.PDB_TYPE].append(pdb_file)

            if pdb_file.PDB_TYPE != Figure.PDB_TYPE:
                for uuid in pdb_file.figures:
                    try:
                        figure_used_by[uuid].add(pdb_file.uuid)
                    except KeyError:
                        figure_used_by[uuid] = set([pdb_file.uuid])

        i = 0
        for pdb_file in pdb_files[Figure.PDB_TYPE]:
            i += 1
            yield i, n, f"Checking ({Figure.PDB_TYPE.title()})"
            pdb_file.compile()
            try:
                pdb_file.used_by = sorted(figure_used_by[pdb_file.uuid])
            except KeyError:
                pass
        for pdb_type in VALID_TYPES:
            if pdb_type == Figure.PDB_TYPE:
                continue
            message = f"Checking ({pdb_type.title()})"
            for pdb_file in pdb_files[pdb_type]:
                i += 1
                yield i, n, message
                pdb_file.compile()

        i = 0
        for pdb_type in VALID_TYPES:
            message = f"Saving ({pdb_type.title()})"
            for pdb_file in pdb_files[pdb_type]:
                i += 1
                yield i, n, message
                self.update(pdb_file)
                pdb_file.save()

        yield 0, 0, "Cleaning"
        metadata_uuids = set(self._pdb_data.keys())
        all_uuids = set(
            tex_file.stem
            for tex_file in config.PDB_DB_DIR.glob('*.tex')
        )
        for uuid in metadata_uuids - all_uuids:
            logger.info(f"Remove {uuid} from metadata")
            del self._pdb_data[uuid]

        for f in config.PDB_DB_DIR.glob('*'):
            if f.suffix in [".aux", ".log"]:
                f.unlink()
            elif (
                f.suffix in [".json", ".pdf", ".pty"]
                and not f.with_suffix(".tex").is_file()
            ):
                logger.info(f"rm {f}")

        self.save()
        Tags.reset_all_tags()
        yield 1, 1, "Completed"

    def save(self) -> None:
        with config.PDB_METADATA_PATH.open('wb') as pkl:
            pickle.dump(self, pkl)

    def filter(
        self,
        query: str,
        file_types: set[str],
        selected_tags: Tags,
        discarded_tags: Tags,
    ) -> list[PDBFile]:
        out = [
            pdb_file
            for pdb_file in self._pdb_data.values()
            if (
                pdb_file.PDB_TYPE in file_types
                and pdb_file.tags.include(selected_tags)
                and pdb_file.tags.exclude(discarded_tags)
            )
        ]
        if query:
            if matched_uuids := greptex(query, config.PDB_DB_DIR, False):
                out = [
                    pdb_file
                    for pdb_file in out
                    if pdb_file.uuid in matched_uuids
                ]
            else:
                return []

        return sorted(out, reverse=True)
