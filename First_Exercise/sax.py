from xml.sax import make_parser, ContentHandler

INPUT_PATH = 'Data/cf79.xml'
OUTPUT_PATH = 'Outputs/titulo.xml'


class TitleHandler(ContentHandler):
    """ Class created to extract the title tag from a given xml
    """

    def __init__(self):
        self.current_data = ""
        self.title = ""

    def startElement(self, tag, _):
        if tag == "TITLE":
            self.current_data = tag

    def endElement(self, _):
        if self.current_data == "TITLE":
            output_file.write(f'<TITLE>{self.title}</TITLE>\n')

        self.current_data = ""
        self.title = ""

    def characters(self, content):
        if self.current_data == "TITLE":
            self.title += content


if __name__ == "__main__":
    parser = make_parser()
    Handler = TitleHandler()

    parser.setContentHandler(Handler)
    with open(OUTPUT_PATH, 'w') as output_file:
        parser.parse(INPUT_PATH)
