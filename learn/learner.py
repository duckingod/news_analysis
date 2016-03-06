from abc import ABCMeta, abstractmethod

class Learner(object):
    """Learner interface
    Attributes:
        name: Model name.
        vectors: inputed vectors.
    """
    __metaclass__ = ABCMeta
    MODEL_PATH = "./data/model/{name}"
    
    def model_path(self):
        """Get model saving path.
            Return:
                path of folder saving model.
        """
        return self.MODEL_PATH.format(name=self.name)

    def set_name(self, name):
        """Set model name.
            Set name of this model.
            Use when saving model.
        """
        self.name = name

    def get_file_name(self, name):
        """Get file name in a model.
            Returns:
                path of file in the model
        """
        import os.path
        return os.path.join(
                self.model_path(),
                name
                )

    @abstractmethod
    def input(self, vectors):
        """ Input to-train or to-predict data.
            Args:
                vector: the inputing list of vector.
            Returns:
                Self
        """
        pass

    @abstractmethod
    def train(self):
        """ Train inputed data, and save model in model_path(self).
            Returns:
                Self
        """
        pass

    @abstractmethod
    def predict(self):
        """ Predict inputed data.
            Returns:
                list of predicted label.
        """
        pass

class LinearLearner(Learner):
    """LinearSVM"""
    def __init__(self):
        from sklearn.svm import LinearSVC
        self.classifier = LinearSVC()
    def input(self, vectors):
        self.vectors = vectors
        x = []
        y = []
        for v in vectors:
            y.append(v[0])
            x.append(v[1])
        self.x = x
        self.y = y
        return self
    def train(self, vectors):
        self.classifier.fit(self.x, self.y)
        return self
    def predict(self):
        return self.classifier.predict(self.x)

