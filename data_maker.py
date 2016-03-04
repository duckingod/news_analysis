from feature.extract import ThresholdLogExtractor
from feature.generate import SimpleNGramGenerator
from model.record_manage import EntryTagManager, LabelTagManager
from model.common import PathGetter

class DataMaker:
    def __init__(self, feature_generator, feature_extractors):
        self.article_mgr = ArticleManager() 
        self.generator = feature_generator
        if type(feature_extractors) is list:
            self.extractors = feature_extractors
        elif feature_extractors==None:
            self.extractors = []
        else:
            self.extractors = [feature_extractors]
    def make(self):
        articles = self.article_mgr.get_articles()
        result = []
        for article in articles:
            label, content = self.article_mgr.get_content(article)
            vector = self.generator.generate(content)
            for extractor in self.extractors:
                vector = extractor.extract(vector)
            result.append([label, vector])
        return (articles, result)

class VectorGenerator:
    def __init__(self,
            config_name,
            article_mgr,
            feature_generator,
            feature_extractors
            ):
        self.name = config_name
        self.article_mgr = article_mgr
        self.generator = feature_generator
        self.extractors = feature_extractors
        path_getter = PathGetter(self.name)
        self.entry_tag = EntryTagManager(path_getter)
        self.label_tag = LabelTagManager(path_getter)
    def generate(self):
        self.data_maker = DataMaker(self.generator, self.extractors)
        articles, vectors = self.data_maker.make()
        result = []
        for v in vectors:
            result_label = []
            result_entry = []
            for label in v[0]:               
                result_label.append(self.label_tag(label))
            for entry in v[1]:
                result_entry.append(
                        (self.entry_tag(entry[0]), entry[1])
                )
            result.append((result_label, result_entry))
        print 'save label/entry tag sheet for ' + self.name
        self.label_tag.save_tag_sheet()
        self.entry_tag.save_tag_sheet()
        return articles, result
                
if __name__=='__main__':
    from model.data_manage import ArticleManager
    from feature.generate import SimpleNGramGenerator
    from feature.extract import ThresholdLogExtractor
    generator = VectorGenerator(
            'ngram-thres_log-test',
            ArticleManager(),
            SimpleNGramGenerator(n=2),
            ThresholdLogExtractor(2, 4))
    articles, vectors = generator.generate()
        
    print '===='
    print articles[0].title
    print vectors[0]


