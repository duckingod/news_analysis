class switch:
    def __init__(self, p):
        self.p = p
        self.inside = False
        self.next_flag = False
    def __call__(self, eq=None, to=None):
        if self.inside:
            return False
        if eq==None  or \
           to==None and self.p==eq  or \
           to!=None and eq<=self.p<=to :
            self.inside = True
            return True

        return False
    def __iter__(self):
        return self
    def next(self):
        if not self.next_flag:
            self.next_flag = True
            return self
        raise StopIteration
