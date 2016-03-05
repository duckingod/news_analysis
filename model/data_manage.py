import glob
import os.path
import datetime
from datetime import timedelta, date

class ArticleInfo:
    def __init__(self, loader_ID=None, article_ID=None, date=None, title=None):
        self.loader_ID  = loader_ID
        self.article_ID = article_ID
        self.date = date
        self.title = title
    def uni_id(self):
        return (self.loader_ID, self.article_ID)

class ArticleManager:
    DATA_PATH = u'data/article'
    LABEL_PATH = u'data/label'
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
        def re_wildcard(self):
            return u"[0-9]{8}-[0-9]{4}-.*.txt"

    nameresolver=NameResolver()

    def __init__(self):
        self.label_sheet_cache = None
    
    def __article_full_path(self, info):
        return os.path.join( self.DATA_PATH, self.nameresolver.name(info) )

    def update(self, loader, result):
        def update_single(info, content):
            from news_site import utils
            file_name = self.__article_full_path(info)
            with open(file_name, 'w') as f:
                f.write(content.encode('utf-8'))
                print 'saved: ' + file_name[:25] + ' ...'
        import Queue
        if isinstance(result, Queue.Queue):
            while not result.empty():
                info, content = result.get()
                update_single(info, content)
        elif type(result) is tuple:
            info, content = result
            update_single(info, content)


    def get_articles(
            self,
            from_time=datetime.datetime.now()-timedelta(1),
            to_time=datetime.datetime.now()+timedelta(1)):
        def daterange(st, end):
            for n in range(int( (end-st).days )):
                yield st + timedelta(n)
        import re
        articles = []
        result = []

        r = re.compile(self.nameresolver.re_wildcard())
        for article in [f for f in os.listdir(self.DATA_PATH) if r.search(f)]:
            info = self.nameresolver.info(article)
            if from_time <= info.date <= to_time:
                result.append(info)
        # for date in daterange(from_time, to_time):
        #      print date
        #     day_articles = glob.glob( os.path.join(self.DATA_PATH, self.nameresolver.day_wildcard(date)) )
        #     for article in day_articles:
        #         info = self.nameresolver.info(article)
        #         if from_time <= info.date <= to_time:
        #             result.append(info)
        return result 

    """
    Get label and text content of article
    param info: article info
    return: (label, text)
    """
    def get_content(self, info):
        path = self.__article_full_path(info)
        with open(path, 'r') as f:
            cont = f.read().decode('utf-8')
        return (self.get_label(info), cont)
    def get_label(self, info):
        return self.__get_label_sheet().get(info.uni_id(), [])
    def __get_label_sheet(self):
        if self.label_sheet_cache!=None:
            return self.label_sheet_cache
        import os.path
        if os.path.isfile(self.LABEL_PATH):
            with open(self.LABEL_PATH, 'r') as f:
                s = f.read().decode('utf-8')
                self.label_sheet_cache = eval(s)
        else:
            self.label_sheet_cache = {}
        return self.label_sheet_cache
    def save_label_sheet(self):
        with open(self.LABEL_PATH, 'w') as f:
            f.write(str(self.label_sheet_cache).encode('utf-8'))
    def set_label(self, info, label):
        self.__get_label_sheet()[info.uni_id()] = label

