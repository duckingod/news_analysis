
def get_all_text(lxml_tree):
    s = ""
    if type(lxml_tree.text) is unicode:
        s += lxml_tree.text
    for node in lxml_tree:
        s += get_all_text(node) + '\n'
    if type(lxml_tree.tail) is unicode:
        s += lxml_tree.tail
    return s

def find_idx(some_list, some_func):
    for idx, cont in enumerate(some_list):
        if some_func(cont):
            return idx
    return len(some_list)

    
def filenamelize(s):
    return s.replace('/', '')
