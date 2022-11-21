from os import environ


class StaticPath:
    def __init__(self):
        self.__cwd: str = environ.get("PWD", ".")

    @property
    def cwd(self) -> str:
        return self.__cwd

    @property
    def assets(self) -> str:
        return f"{self.__cwd}/assets"

    @property
    def templates(self) -> str:
        return f"{self.assets}/templates"

    @property
    def views(self) -> str:
        return f"{self.assets}/views"

    @property
    def styles(self) -> str:
        return f"{self.assets}/styles"

    @property
    def scripts(self) -> str:
        return f"{self.assets}/scripts"

    @property
    def images(self) -> str:
        return f"{self.assets}/images"


static_path: StaticPath = StaticPath()
