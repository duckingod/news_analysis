class PathGetter:
    BASE_PATH = "data/{name}/{prop}"
    def __init__(self, name):
        self.name = name
    def __call__(self, prop):
        return self.BASEPATH.format(name=self.name, prop=prop)

