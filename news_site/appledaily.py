from lxml import etree
import urllib
import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from crawler import SiteLoader

class AppleDailyLoader(SiteLoader):
    # /realtimenews/article/finance/20160228/805101/ <- 46-th
    SITE = "http://www.appledaily.com.tw/realtimenews/section/finance/{0}"
    HOST = "http://www.appledaily.com.tw"
    URL_TITLE_IDX = 45
    def ID(self): return "0000"        

    def __init__(self):
        self.next_index_page = 0
        self.grep_urls = []
        self.next_url_idx = 0
        self.cnt = 0 # debug

    def __get_urls(self, idx):
        def get_article_url_infos(div):
            def to_date(date_s, time_s): 
                import datetime
                return datetime.datetime.strptime(date_s+"-"+time_s[:2]+time_s[-2:], '%Y / %m / %d-%H%M')
            def to_time(s):
                return s[:2]+s[-2:]
            def to_id(s):
                return "0000"+s
            from model.data_manage import ArticleInfo
            infos = []
            urls = []
            for idx, e in enumerate(div):
                if e.tag=="h1":
                    article_list = div[idx+1]
                    date = e.xpath("time")[0].text
                    for article in article_list: # article is 'li'
                        tmpu = article.xpath("a")[0].get("href") 
                        url = tmpu[:self.URL_TITLE_IDX]
                        art_id = url[url.rfind('/')+1:]
                        title = tmpu[self.URL_TITLE_IDX+1:]
                        time = article.xpath("a//time")[0].text
                        infos.append(ArticleInfo(
                            article_ID=to_id(art_id),
                            title=title,
                            date=to_date(date, time)) )
                        urls.append( self.HOST + url )
            return zip(infos, urls)
        index_url = AppleDailyLoader.SITE.format(idx)
        request = urllib.urlopen(index_url)
        html = request.read()
        tree = etree.HTML(html.lower().decode('utf-8'))
        list_div = tree.xpath(
                "//article[@id='maincontent']/div[@class='thoracis']/div")[1]
        self.grep_urls = get_article_url_infos(list_div)

    def next_url(self):
        if self.cnt>5:
            return None
        self.cnt += 1
        if self.next_url_idx >= len(self.grep_urls):
            self.__get_urls(self.next_index_page)
            self.next_index_page += 1
            self.next_url_idx = 0
        if len(self.grep_urls) <= 0:
            return None
        result = self.grep_urls[self.next_url_idx]
        self.next_url_idx += 1
        return result
        
    def fetch_article_content(self, html):
        from news_site.utils import get_all_text, find_idx
        tree = etree.HTML(html.lower().decode('utf-8'))
        e = tree.xpath("//article[@id='maincontent']/div/div/article/div[3]")[0]
        idx = min(find_idx(e, lambda n:n.tag=='iframe'), 
                  find_idx(e, lambda n:n.get('id')=='teadstv'))
        for n in e[idx:]:
            e.remove(n)
        return get_all_text(e).strip()

