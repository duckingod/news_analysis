from data_maker import *
from model.data_manage import ArticleManager
from feature.generate import SimpleNGramGenerator
from feature.extract import ThresholdLogExtractor
article_mgr = ArticleManager()

generator = VectorGenerator(
        'ngram-thres_log-test',
        article_mgr, 
        SimpleNGramGenerator(n=2),
        ThresholdLogExtractor(2, 4))
articles, vectors = generator.generate()
article_mgr.set_label(articles[0],['Label0'])
article_mgr.save_label_sheet()
