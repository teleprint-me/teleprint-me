import json
import os


class DirectoryPath:
    def __init__(self, relative_path: str = ''):
        self.__relative_path: str = relative_path or '.'
        self.__absolute_path: str = os.environ["PWD"]
        self.__entries: list[os.DirEntry] = []
        self.__labels: list[str] = os.listdir(relative_path)

    @property
    def relative_path(self) -> str:
        return self.__relative_path

    @relative_path.setter
    def relative_path(self, value: str):
        self.__relative_path = value

    @property
    def absolute_path(self) -> str:
        return self.__absolute_path

    @property
    def entries(self) -> tuple[os.DirEntry]:
        return tuple(i for i in os.scandir(f"{self.absolute_path}/{self.relative_path}"))

    @property
    def labels(self) -> list[str]:
        return self.__labels

    @property
    def path(self) -> str:
        return os.path.join(self.absolute_path, self.relative_path)

    def getJoinedPaths(self, sort: bool = False) -> list[str]:
        if sort:
            return sorted(
                os.path.join(self.absolute_path, e.path) for e in self.entries
            )
        return [os.path.join(self.absolute_path, e.path) for e in self.entries]

    def getJoinedLists(self, sort: bool = False) -> tuple[tuple[str, os.DirEntry]]:
        if sort:
            return tuple(sorted((l, e) for l, e in zip(self.labels, self.entries)))
        return tuple((l, e) for l, e in zip(self.labels, self.entries))

    def hasMatchedLists(self) -> bool:
        if len(self.entries) != len(self.labels):
            return False
        for label, entry in zip(self.labels, self.entries):
            if entry.path != os.path.join(self.relative_path, label):
                return False
        return True

    def rename(self, prefix: str = "x") -> bool:
        for index, current_path in enumerate(self.getJoinedPaths(True)):
            try:
                extension = os.path.splitext(current_path)[1]
                next_path = os.path.join(self.path, f"{prefix}_{index:03}{extension}")
                os.rename(current_path, next_path)
            except (IsADirectoryError, NotADirectoryError, OSError) as error:
                print(error)
                return False
        return True

    @staticmethod
    def getSplitName(entry) -> tuple[str, str]:
        try:
            label = entry.name.split(".")[0]
            extension = entry.name.split(".")[1]
        except (IndexError,):
            label = entry.name.split(".")[0]
            extension = ""
        return label, extension

    def scan(self, relative_path: str) -> str:
        self.relative_path = relative_path
        self.__entries = []
        for entry in os.scandir(relative_path):
            label, extension = self.split(entry)
            self.__entries.append(
                {
                    "path": f"/{entry.path}",
                    "name": entry.name,
                    "label": label,
                    "extension": extension,
                    "is_dir": entry.is_dir(),
                    "is_file": entry.is_file(),
                }
            )
        return json.dumps(self.__entries)


dir_entity = DirectoryPath()
