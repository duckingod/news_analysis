import glob
import os.path

class ArticleInfo:
    def __init__(self, loader_ID=None, article_ID=None, date=None, title=None):
        self.loader_ID  = loader_ID
        self.article_ID = article_ID
        self.date = date
        self.title = title

class ArticleManager:
    DATA_PATH = u'data/article'
    class NameResolver:
        NAME = u'{date}-{time}-{loader_ID}-{article_ID}-{title}.txt'
        #             20160216-2140-0000-123456890-article_title.txt
        def __datetime_to_date_s(self, date):
            return "%04d%02d%02d" % (date.year, date.month, date.day)
        def __datetime_to_time_s(self, date):
            return "%02d%02d" % (date.hour, date.minute)
        def __s_to_datetime(self, date_s, time_s):
            import datetime
            return datetime.datetime.strptime(date_s+"-"+time_s, "%Y%m%d-%H%M")
        def name(self, info):
            from news_site import utils
            return utils.filenamelize(
                    self.NAME.format(
                            loader_ID=info.loader_ID,
                            article_ID=info.article_ID,
                            title=info.title,
                            date=self.__datetime_to_date_s(info.date),
                            time=self.__datetime_to_time_s(info.date)))
        def info(self, path):
            name = os.path.basename(path)
            tokens = name.split("-")
            info = ArticleInfo(
                    loader_ID = tokens[2],
                    article_ID = tokens[3],
                    date = self.__s_to_datetime(tokens[0], tokens[1]),
                    title = os.path.splitext( ("-".join(tokens[4:])) )[0]
                    )
            return info
        def day_wildcard(self, date):
            return self.__datetime_to_date_s(date) + "-*.txt"

    nameresolver=NameResolver()
    
    def update(self, loader, result):
        from news_site import utils
        loader_ID = loader.ID()
        while not result.empty():
            info, content = result.get()
            file_name = os.path.join( self.DATA_PATH, self.nameresolver.name(info) )
            with open(file_name, 'w') as f:
                f.write(content.encode('utf-8'))
                print 'saved: ' + file_name[:25] + ' ...'
    def get_articles(self, from_time, to_time):
        def daterange(st, end):
            from datetime import timedelta, date
            for n in range(int( (end-st).days )):
                yield st + timedelta(n)
        articles = []
        for date in date_range(from_time, to_time):
            day_articles = glob.glob( os.path.join(self.DATA_PATH, self.nameresolver.day_wildcard(date)) )
            for article in day_articles:
                info = self.article_info_from_name
        
