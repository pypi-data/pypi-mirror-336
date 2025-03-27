import json
from logging import getLogger
from typing import (
    ClassVar,
    Iterator,
    Self,
)

from phystool.config import config

logger = getLogger(__name__)


class Tags:
    TAGS: ClassVar['Tags']

    @classmethod
    def validate(cls, list_of_tags: str) -> Self:
        if not list_of_tags:
            return cls()

        tmp: dict[str, list[str]] = dict()
        for tag in sorted([tag.strip() for tag in list_of_tags.split(',')]):
            valid = False
            for category, tags in cls.TAGS:
                if tag in tags:
                    valid = True
                    try:
                        tmp[category].append(tag)
                    except KeyError:
                        tmp[category] = [tag]
            if not valid:
                logger.warning(f"Invalid tag {tag}")

        return cls(tmp)

    @classmethod
    def list_valid_tags(cls) -> None:
        for _, tags in cls.TAGS:
            for tag in tags:
                print(tag)

    @classmethod
    def save(cls) -> None:
        with config.PDB_TAGS_PATH.open("w") as jsout:
            json.dump(cls.TAGS.data, jsout, indent=4, ensure_ascii=False)

    @classmethod
    def reset_all_tags(cls) -> None:
        data: dict[str, set[str]] = dict()
        for json_file in config.PDB_DB_DIR.glob('*.json'):
            with json_file.open() as jsin:
                for category, tags in json.load(jsin).get('tags', {}).items():
                    if tags:  # so that unused category are removed
                        try:
                            data[category] |= set(tags)
                        except KeyError:
                            data[category] = set(tags)

        all_tags = {
            category: sorted(tags)
            for category, tags in data.items()
        }
        cls.TAGS = Tags(all_tags)
        cls.save()

    @classmethod
    def create_new_tag(cls, category: str, tag: str) -> None:
        if tags := cls.TAGS[category]:
            tags.append(tag)
            tags.sort()
        else:
            cls.TAGS.data[category] = [tag]
        cls.save()

    def __init__(self, tags: dict[str, list[str]] = dict()):
        self.data = tags

    def __getitem__(self, key) -> list[str]:
        return self.data.get(key, [])

    def __iter__(self) -> Iterator[tuple[str, list[str]]]:
        for category, tags in self.data.items():
            yield category, tags

    def __add__(self, other: Self) -> Self:
        out = type(self)(self.data.copy())  # Tags != Self
        out += other
        return out

    def __iadd__(self, other: Self) -> Self:
        self.data = {
            category: tags
            for category in self.TAGS.data.keys()
            if (tags := sorted(set(self[category] + other[category])))
        }
        return self

    def __sub__(self, other: Self) -> Self:
        out = type(self)(self.data.copy())  # Tags != Self
        out -= other
        return out

    def __isub__(self, other: Self) -> Self:
        self.data = {
            category: tags
            for category in self.TAGS.data.keys()
            if (tags := sorted(set(self[category]) - set(other[category])))
        }
        return self

    def __bool__(self) -> bool:
        for tags in self.data.values():
            if tags:
                return True
        return False

    def __str__(self) -> str:
        return ", ".join(self.all())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tags):
            return False

        if len(self.data.keys()) != len(other.data.keys()):
            return False

        for category, tags in self:
            if set(other[category]) != set(tags):
                return False
        return True

    @property
    def cursus(self) -> str:
        return "/".join(self['cursus'])

    @property
    def topic(self) -> str:
        return "/".join(self['topic'])

    @property
    def difficulty(self) -> str:
        return "/".join(self['difficulty'])

    def include(self, other: Self) -> bool:
        return not other or self._contains(other)

    def exclude(self, other: Self) -> bool:
        return not other or not self._contains(other)

    def _contains(self, other: Self) -> bool:
        for category in other.data.keys():
            if set(self[category]).isdisjoint(other[category]):
                return False
        return True

    def all(self) -> list[str]:
        return [
            tag
            for tags in self.data.values()
            for tag in tags
        ]

    def list_tags(self) -> None:
        for tag in self.all():
            print(tag)


if config.PDB_TAGS_PATH.exists():
    with config.PDB_TAGS_PATH.open() as jsin:
        Tags.TAGS = Tags(json.load(jsin))
else:
    Tags.reset_all_tags()
