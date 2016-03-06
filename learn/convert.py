
class LearnTypeConverter(object):
    """Change vectors to desired format.
    example:
        'list of label' change to 2 label fitting '1-n learner'
    """
    def convert(self, vectors):
        """Convert vectors to desired format"""
        pass

class ZeroOneConverter(LearnTypeConverter):
    def __init__(self, label_set):
        """
        Args:
            label_set: the want to predict '1' labels 
        """
        self.label_set = label_set
    def convert(self, vectors):
        result = []
        for v in vectors:
            labels = v[0]
            if [None for l in labels if (labels in self.label_set)]:
                result.append([1, v[1]])
            else:
                result.append([0, v[1]])
        return result 
        
