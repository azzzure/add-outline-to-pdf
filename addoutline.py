from pypdf import PdfReader
from pypdf import PdfWriter

class toc():
    """tree node of outline"""
    def __init__(self, name: str, pagenumber: int):
        
        self.name = name
        self.pagenumber = pagenumber
        self.children = []
        self.parent = None

    def add_child(self, obj):
        self.children.append(obj)
        obj.parent = self

    def children_list(self):
        return self.children

    def __str__(self):
        return f"{self.name} {self.pagenumber}"

    def __repr__(self):
        return f"{self.name} {self.pagenumber}"

    def empty(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def hierarchy(self, level=None):
        '''print outline in hierarchy format'''
        if level == None:
            level = 0
        print("  "*level, self)
        for i in self.children:
            i.hierarchy(level=level+1)

    def add_outline_to_writer(self, writer, parent=None):
        '''traverse the outline tree, add to a Pdfwriter'''
        print(f"<{self.name}>")
        if parent == None:
            # root node should be added
            ido = writer.get_outline_root()
        else:
            ido = writer.add_outline_item(
                title=self.name, page_number=self.pagenumber, parent=parent)
        for i in self.children:
            i.add_outline_to_writer(writer, parent=ido)
        return ido


def parseline(s):
    """parse lines of outline\n
    a line is composed as \n
    {space}*n+{title}+{space}+{page number}\n
    return value is a tuple int,str,int"""
    space_length = 0
    #count how much space from beginning
    for c in s:
        if c == " ":
            space_length = space_length+1
            continue
        else:
            break
    #extract page numer from end
    page_number_index = len(s)-1
    while s[page_number_index] != ' ':
        page_number_index = page_number_index-1
    #remaining part is title
    title = s[space_length:page_number_index]
    page_number = int(s[page_number_index+1:])
    # print(f">{s}< --> {space_length,title,page_number}")
    return (space_length, title, page_number)


def strtotoc(tocstring, offset=0):
    '''turn table of contens string to a tree\n'''
    lines = tocstring.split("\n")
    root = toc("root", -1)
    currentlevel = 0
    previous = None
    parent = root
    for line in lines:
        level, title, page_numer = parseline(line)
        me = toc(title, pagenumber=page_numer+offset)
        if currentlevel == level:
            print(f"{level,title,page_numer} stay parent: {parent} ")
            parent.add_child(me)

        if currentlevel > level:
            # go back to parent level
            print(f"{level,title,page_numer} back parent: {parent} ")
            path = currentlevel-level
            # there may be more than one level
            while(path != 0):
                parent = parent.parent
                path = path-1
            currentlevel = level
            parent.add_child(me)

        if currentlevel < level:
            # go to nexet level
            print(f"{level,title,page_numer} forward parent: {parent} ")
            currentlevel = level
            parent = previous
            parent.add_child(me)
        previous = me
    return root


def addtoc(tocstring:str, pdfname:str, offset:int=0):
    '''given a table of contents string and pdf filename\n
    add clickable table of contents to pdf file
    some times page number may point to wrong position, add offset.
    '''
    reader = PdfReader(pdfname)
    writer = PdfWriter()
    writer.append(reader, import_outline=False)
    table_of_content = strtotoc(tocstring, offset=offset)
    table_of_content.hierarchy()
    table_of_content.add_outline_to_writer(writer)
    writer.write('added.pdf')

