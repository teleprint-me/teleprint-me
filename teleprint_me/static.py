from os import environ


class EnvironPath(object):
    def __init__(self):
        self.__cwd: str = environ.get("PWD", ".")

    @property
    def cwd(self) -> str:
        return self.__cwd

    @property
    def root(self) -> str:
        return self.__root

    @root.setter
    def root(self, name: str):
        self.__root = name


class StaticPath(EnvironPath):
    def __init__(self, root: str = ""):
        super(StaticPath, self).__init__()

        self.root: str = root

    @property
    def directory(self) -> str:
        if self.root:
            return f"{self.cwd}/{self.root}"
        return f"{self.cwd}/static"

    def get(self, name: str) -> str:
        return f"{self.directory}/{name}"

    @property
    def views(self) -> str:
        return self.get("views")

    @property
    def templates(self) -> str:
        return self.get("templates")

    @property
    def styles(self) -> str:
        return self.get("styles")

    @property
    def scripts(self) -> str:
        return self.get("scripts")

    @property
    def images(self) -> str:
        return self.get("images")


class ModulePath(EnvironPath):
    def __init__(self, root: str = ""):
        super(ModulePath, self).__init__()

        self.root: str = root

    @property
    def directory(self) -> str:
        if self.root:
            return f"{self.cwd}/{self.root}"
        return f"{self.cwd}/modules"

    def get(self, name: str) -> str:
        return f"{self.directory}/{name}"

    @property
    def grassroots(self) -> str:
        return self.get("grassroots")


static_path: StaticPath = StaticPath()
module_path: ModulePath = ModulePath()
