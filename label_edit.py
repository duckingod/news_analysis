from model.data_manage import ArticleManager
import curses

import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding() 
 
from utils import switch

"""
self: run(self, c)
      stdscr
      height
"""
def while_run(self):
    while self.run(self.stdscr.getch(self.height, 0)):
        pass

class ArticleViewer(object):
    WIN_Y_START = 3
    WIN_X_START = 10
    WIN_WIDTH = 49
    WIN_HEIGHT = 15
    LABEL_HEIGHT = 3
    def __init__(self, article_mgr, stdscr):
        self.article_mgr = article_mgr
        self.stdscr = stdscr
    def clear_window(self):
        for i in range(self.WIN_HEIGHT):
            self.window.addstr(i, 0, ' '*self.WIN_WIDTH)
    def show_label(self, label):
        s = "  ".join([str(i)+":"+l for i, l in enumerate(label)])
        self.window.addstr(1, 1, s)
    def show_content(self, s):
        w = self.WIN_WIDTH+-10
        for i in range(0, (len(s)+w-1)/w, w):
            if self.LABEL_HEIGHT+i/w>=self.WIN_HEIGHT:
                break
            self.window.addstr(self.LABEL_HEIGHT+i/w, 1, s[i:i+w].ljust(w))
    def update_article(self):
        article = self.article_list_viewer.selected_article()
        label, cont = self.article_mgr.get_content(article)
        self.clear_window()
        self.show_label(label)
        self.show_content(cont.encode(code))
        self.window.box()
        self.window.refresh()
    def start(self, article_list_viewer):
        self.article_list_viewer = article_list_viewer
        self.height = self.article_list_viewer.height
        self.window = curses.newwin(self.WIN_HEIGHT, self.WIN_WIDTH+1, self.WIN_Y_START, self.WIN_X_START)
        if self.window==None:
            exit()
        self.stdscr.refresh()
        self.article_list_viewer.set_force_top(True)
        self.update_article()

        while_run(self)

        self.article_list_viewer.set_force_top(False)
        self.window = None

    def run(self, c):
        if c==ord('q') or c==ord(' '):
            return False
        else:
            b = self.article_list_viewer.run(c)
            self.update_article()
            return b 
        return True

class QuickLabelSetMaintainer(object):
    POSITION = [5, 50, 5, 6]
    # height, width, off_x, off_y
    def __init__(self, stdscr):
        self.label = ['']*10
        self.stdscr = stdscr
        self.show_str = ""
    def refresh(self, show_s=None):
        if show_s:
            self.show_str = show_s
        ss = [ self.show_str,
              "  ".join([str(i  )+":"+l for i, l in enumerate(self.label[ : 5])]),
              "  ".join([str(i+5)+":"+l for i, l in enumerate(self.label[5:10])]) ]
        for i, s in enumerate(ss):
            self.window.addstr(i+1, 1, s.ljust(self.POSITION[1]))
        self.window.box()
        self.window.refresh()
    def start(self, article_list_viewer):
        self.window = curses.newwin(self.POSITION[0], self.POSITION[1], self.POSITION[2], self.POSITION[3])
        self.height = article_list_viewer.height
        self.stdscr.refresh()
        self.refresh()

        while_run(self)
    def run(self, ch):
        for c in switch(ch):
            if c(ord('0'), ord('9')):
                self.refresh("Input new Label for '"+chr(ch)+"'")
                l = self.stdscr.getstr()
                self.label[ch-ord('0')] = l
            if c(ord('q')):
                return False
        self.refresh("Press 0~9 for editing corresponding label")
        return True
        
        


        
        

class ArticleListViewer(object):
    # >  001301 2016/02/16 21:34 Title================
    INFO_FORMAT = "{index} {year}/{month}/{day} {hour}:{minute} {title}"
    INFO_PREFIX = 4
    INFO_WIDTH = 75
    INDEX_LENGTH = 6
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 22
    def __init__(self, article_mgr, article_viewer, label_set, stdscr):
        self.top = 0
        self.now = 0
        self.height = self.SCREEN_HEIGHT
        self.article_mgr = article_mgr
        self.article_viewer = article_viewer
        self.stdscr = stdscr
        self.force_top = False
        self.label_set = label_set
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
    def set_force_top(self, b):
        self.force_top = b
        if b:
            self.move('stay')
            self.refresh()
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
                    title = info.title.encode(code)[:self.INFO_WIDTH-2-2-2-2-4-6-6]
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
            move = self.cursor_pos()-2
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
        while_run(self)
    def run(self, ch):
        for c in switch(ch):
            if c(ord('w')):
                self.move('up')
            if c(ord('s')):
                self.move('down')
            if c(ord('a')):
                self.move('pageup')
            if c(ord('d')):
                self.move('pagedown')
            if c(ord('q')):
                return False
            if c(ord(':')):
                idx = self.stdscr.getstr()
                self.goto(int(idx))
            if c(ord(' ')):
                self.article_viewer.start(self)
                self.refresh()
            if c(ord('c')):
                self.label_set.start(self)
                self.refresh()
            if c():
                return True
        self.window.refresh()
        self.input_cursor_clear()
        return True
    

class LabelEditor(object):
    def __init__(self, article_mgr):
        self.article_mgr = article_mgr
        self.stdscr = curses.initscr()
        self.label_set = QuickLabelSetMaintainer(self.stdscr)
        self.article_viewer = ArticleViewer(self.article_mgr, self.stdscr)
        self.article_list_viewer = ArticleListViewer(self.article_mgr, self.article_viewer, self.label_set, self.stdscr) 
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
        
    

