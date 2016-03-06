from learn.learner import LinearLearner
from learn.convert import ZeroOneConverter
from model.data_manage import ArticleManager
from feature.generate import NGramGenerator
from feature.extract import ThresholdLogExtractor
from data_maker import VectorGenerator
if __name__=="__main__":
    article_mgr = ArticleManager()
    feature_generator = NGramGenerator()
    feature_extractor = ThresholdLogExtractor(2, 5)
    vector_generator = VectorGenerator(
            'ngram-thres_log-test',
            article_mgr,
            feature_generator,
            feature_extractor)
    vectors = vector_generator.generate()
    test_ratio = 0.3
    test_vectors = vectors[ : len(vectors)*test_ratio]
    train_vectors = vectors[len(vectors)*test_ratio+1 : ]
    
    cls_label_set = [
            vector_generator.label_tag('sharp'),
            vector_generator.label_tag('foxconn')
            ]
    convert01 = ZeroOneConverter(cls_label_set)
    train_vectors = convert01.convert(train_vectors)
    test_vectors = convert01.convert(test_vectors)
    learner = LinearLearner()
    learner.input(train_vectors).train()
    result = learner.input(test_vectors).predict()
    cnt = 0
    for label, predict in zip([v[0] for v in test_vectors], result): 
        print "original:", label, "   ", "predict:", predict
        if predict == label:
            cnt += 1
    print "corrent: ", cnt*1.0/len(test_vectors), "%"

            

    

    
        
    
    
