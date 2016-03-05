from model.data_manage import ArticleManager
import curses

class LabelEditor(object):
    # >  001301 2016/02/16 21:34 Title================
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
        print 'loading article done'

    def chk_range(self, position):
        return position<0 or position>=self.height
    def chk_all_range(self, pos):
        return pos<0 or pos>=len(self.articles)
    def make_in_all_range(self, pos):
        return max( min(pos, len(self.articles)-1), 0)
    def cursor_pos(self):
        return self.now-self.top
    def max_top(self):
        return len(self.articles)-self.height
    def show_article(self, index, position):
        if self.chk_range(position): return
        s = ''
        if not self.chk_all_range(index):
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
        if to==None:
            return
        self.clear_prefix(self.now-self.top)
        self.now = self.make_in_all_range(to)
        self.draw_cursor()
    def move(self, direction):
        if direction=='up':
            self.cursor_move(offset=-1)
        elif direction=='down':
            self.cursor_move(offset= 1)
        elif direction=='pageup':
            self.cursor_move(offset=-self.height)
        elif direction=='pagedown':
            self.cursor_move(offset=self.height)
        if self.now<self.top:
            move = -min(self.height, self.top)
        elif self.now>=self.top+self.height:
            move = min(self.height, self.max_top()-self.top)
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
    def goto(self, to):
        if self.chk_all_range(to): return
        self.now = to
        self.top = self.now-5
        if self.top>self.max_top():
            self.top = self.max_top()
        if self.top<0:
            self.top = 0
        self.refresh()
        

    def input_cursor_clear(self):
        self.window.addstr(self.height, 0, ' '*self.SCREEN_WIDTH)
        curses.setsyx(self.height, 0)
        
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
            elif c==ord('a'):
                self.move('pageup')
            elif c==ord('d'):
                self.move('pagedown')
            elif c==ord('q'):
                break
            elif c==ord(':'):
                idx = self.stdscr.getstr()
                self.goto(int(idx))
            self.window.refresh()
            self.input_cursor_clear()
        
            
if __name__=='__main__':
    print '=====Buggy on OSX! Will mess up terminal====='
    print 'press enter to continue (ctrl+c to exit)'
    raw_input()
    
    editor = LabelEditor(ArticleManager())

    print 'press enter to continue'
    raw_input()

            
    editor.run()
        
    

