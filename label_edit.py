from model.data_manage import ArticleManager
import curses

class ArticleViewer(object):
    WIN_Y_START = 1
    WIN_X_START = 6
    WIN_WIDTH = 60
    WIN_HEIGHT = 12
    LABEL_HEIGHT = 2
    def __init__(self, article_mgr, stdscr):
        self.article_mgr = article_mgr
        self.stdscr = stdscr
    def clear_window(self):
        for i in range(self.WIN_HEIGHT):
            self.window.addstr(i, 0, ' '*self.WIN_WIDTH)
    def show_label(self, label):
        s = "  ".join([str(i)+":"+l for i, l in enumerate(label)])
        self.window.addstr(0, 0, s)
    def show_content(self, s):
        self.window.addstr(self.LABEL_HEIGHT, 0, s)
    def update_article(self):
        article = self.article_list_viewer.selected_article()
        label, cont = self.article_mgr.get_content(article)
        self.clear_window()
        self.show_label(label)
        # self.show_content(cont)
        self.show_content("aa")
        self.window.refresh()
    def start(self, article_list_viewer):
        self.article_list_viewer = article_list_viewer
        self.window = curses.newwin(self.WIN_HEIGHT, self.WIN_WIDTH+1, self.WIN_Y_START, self.WIN_X_START)
        self.stdscr.refresh()
        self.article_list_viewer.force_top = True
        self.article_list_viewer.move('stay')
        self.article_list_viewer.refresh()
        self.article_list_viewer.window.refresh()
        self.update_article()
        self.window.refresh()
        while self.run(self.stdscr.getch(self.article_list_viewer.height, 0)):
            pass
        self.article_list_viewer.force_top = False
        self.window = None
    def run(self, c):
        if c==ord('q') or c==ord(' '):
            return False
        else:
            b = self.article_list_viewer.run(c)
            self.update_article()
            return b 
        return True

        
        
    

class ArticleListViewer(object):
    # >  001301 2016/02/16 21:34 Title================
    INFO_FORMAT = "{index} {year}/{month}/{day} {hour}:{minute} {title}"
    INFO_PREFIX = 4
    INFO_WIDTH = 60
    INDEX_LENGTH = 6
    SCREEN_WIDTH = 70
    def __init__(self, article_mgr, article_viewer, stdscr):
        self.top = 0
        self.now = 0
        self.height = 15
        self.article_mgr = article_mgr
        self.article_viewer = article_viewer
        self.stdscr = stdscr
        self.force_top = False
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
    def selected_article(self):
        return self.articles[self.now]
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
        s = s.ljust(self.INFO_WIDTH)
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
        self.clear_prefix(self.cursor_pos())
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
        elif direction=="stay":
            self.cursor_move(offset=0)

        if self.force_top:
            move = self.cursor_pos()
        else:
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
        self.window.refresh()
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
    def start(self):
        self.window = curses.newwin(self.height+2, self.SCREEN_WIDTH+1)
        self.window.addstr(0, 0, 'loading article info...')
        self.articles = self.article_mgr.get_articles()
        self.stdscr.refresh()
        self.refresh()
        while self.run(self.stdscr.getch(self.height, 0)):
            pass
    def run(self, c):
        if c==ord('w'):#curses.KEY_UP:
            self.move('up')
        elif c==ord('s'):#curses.KEY_DOWN:
            self.move('down')
        elif c==ord('a'):
            self.move('pageup')
        elif c==ord('d'):
            self.move('pagedown')
        elif c==ord('q'):
            return False
        elif c==ord(':'):
            idx = self.stdscr.getstr()
            self.goto(int(idx))
        elif c==ord(' '):
            self.article_viewer.start(self)
            self.refresh()
        self.window.refresh()
        self.input_cursor_clear()
        return True
    

class LabelEditor(object):
    def __init__(self, article_mgr):
        self.article_mgr = article_mgr
        self.stdscr = curses.initscr()
        self.article_viewer = ArticleViewer(self.article_mgr, self.stdscr)
        self.article_list_viewer = ArticleListViewer(self.article_mgr, self.article_viewer, self.stdscr) 
    def start(self):
        self.article_list_viewer.start()
        curses.endwin()
        print "editor exited"



        
            
if __name__=='__main__':
    print '=====Buggy on OSX! Will mess up terminal====='
    print 'press enter to continue (ctrl+c to exit)'
    raw_input()
    
    editor = LabelEditor(ArticleManager())


            
    editor.start()
        
    

