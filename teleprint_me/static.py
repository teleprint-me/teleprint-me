from os import environ


class StaticPath:
    def __init__(self, root: str = ""):
        self.__root: str = root
        self.__cwd: str = environ.get("PWD", ".")

    @property
    def cwd(self) -> str:
        return self.__cwd

    @property
    def root(self) -> str:
        return self.__root

    @property
    def directory(self) -> str:
        if self.root:
            return f"{self.cwd}/{self.root}"
        return f"{self.cwd}/static"

    def get(self, name: str) -> str:
        return f"{self.directory}/{name}"


class ModulePath(StaticPath):
    def __init__(self, root: str = ""):
        super(ModulePath, self).__init__(root=root)

    @property
    def directory(self) -> str:
        if self.root:
            return f"{self.cwd}/{self.root}"
        return f"{self.cwd}/modules"


static_path: StaticPath = StaticPath()
module_path: ModulePath = ModulePath()
