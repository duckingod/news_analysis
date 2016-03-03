from feature.extract import ThresholdLogExtractor
from feature.generate import SimpleNGramGenerator

class DataMaker:
    def __init__(self, feature_generator, feature_extractors):
        self.article_mgr = ArticleManager() 
        self.generator = feature_generator
        if type(feature_extractors) is list:
            self.extracters = feature_extractors
        else:
            self.extracters = [feature_extractors]
    def make(self):
        articles = self.article_mgr.get_articles()
        result = []
        for article in articles:
            content = self.article_mgr.get_content(article)
            vector = self.feature_generator.generate(content)
            for extractor in self.feature_extractors:
                vector = extractor.extract(vector)
            result.append([article_mgr.get_label(article), vector])
        return vector

class VectorGenerator:
    def __init__(self,
            config_name,
            article_mgr,
            feature_generator,
            feature_extractors
            ):
        self.name = config_name
        self.article_mgr = article_mgr
        self.generator = feature_extractors
        self.extractors = feature_extractors
        self.entry_tag = EntryTagManager(name)
        self.label_tag = LabelTagManager(name)
    def generate(self):
        from model.common import PathGetter
        self.data_maker = DataMaker(self.generator, self.extractors)
        path_getter = PathGetter(self.name)
        self.entry_tag = EntryTagManager(path_getter)
        self.label_tag = LabelTagManager(path_getter)
        vectors = self.data_maker.make()
        result = []
        for v in vectors:
            for l in self.article_mgr.get_label():

            
            
        


        


