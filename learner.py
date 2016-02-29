from model.record_manage import *

def simple_2_gram(s):
    import operator
    d = {}
    for i in range(len(s)-1):
        gram = (s[i], s[i+1])
        d[gram] = d.get(gram, 0) + 1
    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_d
        
def gram_threshold_filter(grams, thres=2):
    return [g for g in grams if g[1]>=thres]

if __name__=="__main__":
    import data_manage
    manager = data_manage.ArticleManager()
    articles = manager.get_articles()
    entry_tag_manager = EntryTagManager()
    print 'now have ', len(entry_tag_manager.tag_sheet()), ' entry tags'
    record_manager = RecordManager()
    for a in articles:
        cont = manager.get_content(a)
        grams = gram_threshold_filter(simple_2_gram(cont), 3)
        print "   ".join([g[0][0]+g[0][1]+" "+str(g[1]) for g in grams])
        print 
        print record_manager.get_vector(grams, entry_tag_manager)
        print 
        print 
    entry_tag_manager.save_tag_sheet()
        
        


