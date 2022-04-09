import xml.sax

class TitleHandler(ContentHandler):
    INPUT_PATH = 'First_Exercise/Data/cf79.xml'
    OUTPUT_PATH = 'First_Exercise/Outputs/autores.xml'

    def __init__(self):
        self.current_data = ""
        self.title = ""
        
    def startElement(self, tag, attributes):
        if tag == "TITLE":
            current_data = tag

    def endElement(self, tag):
        if self.currentTag == "TITLE":
            output_file.write(f'<TITLE>{self.title}</TITLE>\n')

if __name__ == "__main__":
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # override the default ContextHandler
    Handler=TitleHandler()
    parser.setContentHandler(Handler)
    parser.parse(Handler.INPUT_PATH)