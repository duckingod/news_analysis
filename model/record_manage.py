from abc import ABCMeta, abstractmethod


class RecordManager:
    def get_vector(self, record, entry_tag):
        vec = {}
        for entry in record:
            vec[entry_tag.get_tag(entry[0])] = entry[1]
        return vec

class TagManager:
    @abstractmethod
    def tag_sheet_path(self):
        pass
    def __init__(self):
        self.tag_sheet_cache = None
    def tag_sheet(self):
        if self.tag_sheet_cache==None:
            self.tag_sheet_cache = self.__load_tag_sheet()
        return self.tag_sheet_cache

    # TODO should use pickle?
    def __load_tag_sheet(self):
        try:
            f = open(self.tag_sheet_path(), 'r') 
            cont = f.read()
            return eval(cont)
        except:
            print 'generate a new tag sheet for ' + self.tag_sheet_path()
            self.new_tag_sheet()
        return self.tag_sheet()
    def save_tag_sheet(self):
        with open(self.tag_sheet_path(), 'w') as f:
            f.write(str(self.tag_sheet()).encode('utf-8'))
    # COULD Mutate tag sheet
    def get_tag(self, obj):
        if obj not in self.tag_sheet():
            self.tag_sheet()[obj] = len(self.tag_sheet())
        return self.tag_sheet()[obj]
    def new_tag_sheet(self):
        self.tag_sheet_cache = {}
    def remove_tags(self, tag_list, reorder=False):
        for tag in tag_list:
            del self.tag_sheet()[tag]
        if reorder:
            sorted_sheet = sorted(self.tag_sheet().items(), key=operator.itemgetter(1))
            self.new_tag_sheet()
            for item in sorted_sheet:
                self.get_tag(item[0])


class EntryTagManager(TagManager):
    def __init__(self, path_getter):
        self.path_getter = path_getter
    def tag_sheet_path(self):
        return self.path_getter('entry_tag')

class LabelTagManager(TagManager):
    def __init__(self, path_getter):
        self.path_getter = path_getter
    def tag_sheet_path(self):
        return self.path_getter('label_tag')

