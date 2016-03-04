from abc import ABCMeta, abstractmethod

class VectorGenerator:
    __metaclass__ = ABCMeta 
    """
    Generate vector from a string
    """
    @abstractmethod
    def generate(self, content):
        pass

class SimpleNGramGenerator(VectorGenerator):
    def __init__(self, n=2):
        self.n = n
    def generate(self, content):
        import operator
        d = {}
        s = content
        n = self.n
        for i in range(len(s)-(n-1)):
            gram = tuple([s[i+j] for j in range(n)])
            d[gram] = d.get(gram, 0) + 1
        sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_d

