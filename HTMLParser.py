from html.parser import HTMLParser
from html.entities import name2codepoint
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hit = False
        self.temp_func = ""
        self.functions = ""
        self.is_style_tag = False
        self.target_classes = []
    def handle_starttag(self, tag, attrs):
        if tag =="span":
            for attr in attrs:
                if attr[0]=="class" and attr[1] in self.target_classes:
                    self.hit = True
        if tag =="style":
            self.is_style_tag = True
        else:
            self.is_style_tag = False
    def handle_endtag(self, tag):
        global Functions
        if self.hit and not self.temp_func=="":
            #print(self.temp_func)
            self.functions+=(self.temp_func)+"\n"
        self.hit=False        
        #self.function.append(temp_func)
        #print(self.temp_func)
        self.temp_func = ""
        #print("End tag  :", tag)
    def handle_data(self, data):
        if self.hit:
            #print("Data     :", data)
            self.temp_func +=data
        if self.is_style_tag:
            #print(data)
            #print(get_class_id_from_css(data))
            self.target_classes = get_class_ids_from_css(data)
    def handle_entityref(self, name):
        if self.hit:
            c = chr(name2codepoint[name])
            if not c.strip()=='':
                self.temp_func +=c
                #print("Named ent:", c)
################################################
# 
def get_class_ids_from_css(css):
    target_classes = []
    target_font = "Courier New"
    
    while(len(css)):
        i = css.find(target_font)
        if i>=0:
            j= css[0:i].rfind("{")
            k = css[0:j].rfind(".")
            target_classes.append(css[k+1:j])
            css = css[i+1:]
        if i==-1:
            css=""
    return target_classes

def get_program_text_from_html(filename):
    parser = MyHTMLParser()
    with open (filename, "r") as myfile:
        data=myfile.read().replace('\n', '')
    parser.feed(data)
    return parser.functions
#filename = "/Users/qianjizheng/Documents/Projects/LEDParser/E2.html"
#print(get_program_text_from_html(filename))
#tree = etree.parse(filename)
#print(tree)
