from abc import ABCMeta, abstractmethod

class FeatureExtractor:
    __metaclass__ = ABCMeta 
    """
    Extract features from vector.
    return: extracted vector
    """
    @abstractmethod
    def extract(self, vector):
        pass
        
class ThresholdLogExtractor(FeatureExtractor):
    def __init__(self, threshold, logged_max):
        self.threshold = threshold
        self.logged_max = logged_max
    def extract(self, vector):
        import math
        res = []
        for entry in vector:
            val = entry[1]
            if (entry[1]<self.threshold):
                continue
            res.append((entry[0], min(1, math.log(val-self.threshold+2, 2)/self.logged_max)))
        return res
