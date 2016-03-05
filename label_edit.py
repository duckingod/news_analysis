from model.data_manage import ArticleManager
import curses

class LaeblEditor(object):
    # > 2016/02/16 21:34 Title================
    INFO_FORMAT = "{index} {year}/{month}/{day} {hour}:{minute} {title}"
    INFO_PREFIX = 4
    INFO_WIDTH = 40
    INDEX_LENGTH = 6
    SCREEN_WIDTH = 80
    def __init__(self, article_mgr):
        print 'loading article info...'
        self.top = 0
        self.now = 0
        self.height = 15
        self.article_mgr = article_mgr
        self.articles = self.article_mgr.get_articles()

    def chk_range(self, position):
        return position<0 or position>=self.height
    def cursor_pos(self):
        return self.now-self.top
    def show_article(self, index, position):
        if self.chk_range(position): return
        s = ''
        if 0 <= index < len(self.articles):
            info = self.articles[index]
            s += self.INFO_FORMAT.format(
                    index = str(index).zfill(self.INDEX_LENGTH),
                    year  = info.date.year,
                    month = str(info.date.month).rjust(2),
                    day   = str(info.date.day).rjust(2),
                    hour  = str(info.date.hour).rjust(2),
                    minute= str(info.date.minute).rjust(2),
                    title = 'title'#info.title
                    )
        s = (s+' '*self.INFO_WIDTH)[:self.INFO_WIDTH]
        self.window.addstr(
                position,
                self.INFO_PREFIX,
                s)
    def clear_prefix(self, position):
        if self.chk_range(position): return
        self.window.addstr(position, 0, ' '*(self.INFO_PREFIX))
    def draw_cursor(self, cursor_type=None):
        if self.chk_range(self.cursor_pos()): return
        self.window.addstr(self.cursor_pos(), 0, ' > ') 
    def cursor_move(self, to=None, offset=None):
        if offset!=None:
            to = self.now+offset
        if to==None or to>=len(self.articles) or to<0:
            return
        self.clear_prefix(self.now-self.top)
        self.now = to
        self.draw_cursor()
    def move(self, direction):
        if direction=='up':
            self.cursor_move(offset=-1)
        elif direction=='down':
            self.cursor_move(offset= 1)
        if self.now<self.top:
            move = -min(self.height, self.top)
        elif self.now>=self.top+self.height:
            move = min(self.height, len(self.articles)-self.top-self.height)
        else:
            move = 0
        if move!=0:
            self.top += move
            self.refresh()
    def refresh(self):
        for i in range(self.height):
            self.clear_prefix(i)
            self.show_article(self.top+i, i)
        self.draw_cursor()

    def input_cursor_clear(self):
        #self.window.addstr(self.height, 0, ' '*self.SCREEN_WIDTH)
        #curses.setsyx(self.height, 0)
        pass
        
    def run(self):
        self.stdscr = curses.initscr()
        self.window = curses.newwin(self.height+2, self.SCREEN_WIDTH+1)
        self.refresh()
        self.input_cursor_clear()
        while True:
            c = self.stdscr.getch(self.height, 0)
            if c==ord('w'):#curses.KEY_UP:
                self.move('up')
            elif c==ord('s'):#curses.KEY_DOWN:
                self.move('down')
            elif c==ord('q'):
                self.window.close()
            self.window.refresh()
            self.input_cursor_clear()
        
            
if __name__=='__main__':
    editor = LaeblEditor(ArticleManager())
            
    editor.run()
        
    

