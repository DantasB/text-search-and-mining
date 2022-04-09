from xml.sax import make_parser, ContentHandler

INPUT_PATH = 'Data/cf79.xml'
OUTPUT_PATH = 'Outputs/titulo.xml'


class TitleHandler(ContentHandler):
    """ Class created to extract the title tag from a given xml
    """

    def __init__(self):
        self.current_data = ""
        self.title = ""
        self.titles = []

    def startElement(self, tag, _):
        if tag == "TITLE":
            self.current_data = tag

    def endElement(self, _):
        if self.current_data == "TITLE":
            self.titles.append(f'<TITLE>{self.title}</TITLE>\n')

        self.current_data = ""
        self.title = ""

    def characters(self, content):
        if self.current_data == "TITLE":
            self.title += content

    @staticmethod
    def write_elements_to_archive(titles: str, path: str) -> None:
        """Given a string with elements, write it to an archive
        Args:
            titles (str): The elements to be written in the path
            path (str): The path where the elements will be written
        """
        with open(path, 'w') as output:
            output.write(''.join(titles))


if __name__ == "__main__":
    parser = make_parser()
    Handler = TitleHandler()

    parser.setContentHandler(Handler)
    parser.parse(INPUT_PATH)
    Handler.write_elements_to_archive(Handler.titles, OUTPUT_PATH)
