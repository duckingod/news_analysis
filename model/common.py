
class PathGetter:
    BASE_PATH = "./data/{name}/{prop}"
    def __init__(self, name):
        self.name = name
        self.path = self.BASE_PATH.format(
                name=self.name,
                prop='{prop}'
                )
        self.__makedir(self.path)
    def __call__(self, prop):
        return self.path.format(prop=prop)
    def __makedir(self, p):
        from os.path import isdir, dirname
        from os import mkdir
        if not isdir(dirname(p)):
            mkdir(dirname(p))
            self.__makedir(dirname(p))

