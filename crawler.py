from abc import ABCMeta, abstractmethod
from threading import Thread
import subprocess
import urllib
import sys
import os.path
import Queue
import traceback
from model import data_manage


class SiteLoader:
    __metaclass__ = ABCMeta

    """
        Get next article url.
        return: 
            (info, url)  if got next url
            None         if load ends
    """
    @abstractmethod
    def next_url(self):
        pass
    @abstractmethod
    def fetch_article_content(self, html):
        pass
    @abstractmethod
    def ID(self):
        pass

class Crawler:
    class LoadArticleThread(Thread):
        def __init__(self, ID, site_loader, url_queue, result_queue):
            super(Crawler.LoadArticleThread, self).__init__()
            self.ID = ID
            self.loader = site_loader
            self.urls = url_queue
            self.result = result_queue
            self.process = None
            self._stop = False
        def run(self):
            while not self._stop:
                try:
                    info, url = self.urls.get(timeout=1)
                    info.loader_ID = self.loader.ID()
                except:
                    continue
                try:
                    print 'task '+str(self.ID)+' : url get : ' + info.article_ID
                    request = urllib.urlopen(url)
                    html = request.read()
                    content = self.loader.fetch_article_content(html)
                    self.result.put((info, content))
                    print 'task '+str(self.ID)+' : result put : ' + info.article_ID
                except Exception as ea:
                    traceback.print_exc()
                    print ea
                finally:
                    self.urls.task_done()
                    print 'task '+str(self.ID)+' : done : ' + info.article_ID
        def stop(self):
            self._stop = True

    MAX_THREAD = 5
    def __init__(self, site_loader):
        self.threads = []
        self.urls = Queue.Queue()
        self.results = Queue.Queue()
        self.max_threads = Crawler.MAX_THREAD
        self.loader = site_loader
    def __make_threads(self):
        for i in range(self.max_threads):
            self.threads.append(
                    Crawler.LoadArticleThread(
                        i,
                        self.loader,
                        self.urls,
                        self.results
                    )
                )
    def __start_threads(self):
        for thread in self.threads:
            thread.start()
    def __stop_threads(self):
        for thread in self.threads:
            thread.stop()
    def __number_alive_threads(self):
        return sum( [1 for t in self.threads if t.isAlive()] )

    def run(self):
        self.__make_threads()
        self.__start_threads()
        cnt = 0
        while True:
            url_info = self.loader.next_url()
            if url_info==None:
                break 
            (info, url) = url_info
            print 'main: url put ' + str(cnt)
            cnt += 1
            self.urls.put((info, url))
        print 'main: wait join'
        self.urls.join() # results is ok now
        self.__stop_threads()
        return self.results

if __name__=="__main__":
    from news_site.appledaily import AppleDailyLoader

    loader = AppleDailyLoader()
    crawler = Crawler(loader)
    result = crawler.run()
    data_manage.ArticleManager().update(loader, result)
    
