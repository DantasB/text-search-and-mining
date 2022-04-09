from xml.dom.minidom import parse

INPUT_PATH = 'First_Exercise/Data/cf79.xml'
OUTPUT_PATH = 'First_Exercise/Outputs/autores.xml'

def extract_authors_from_xml(path: str) -> str:
    """Extract the authors tag from a given xml
    Args:
        path (str): The path where the xml is located
    
    Returns:
        List: A list containing all the authors tags
    """
    output = []
    docs = parse(path)
    authors = docs.getElementsByTagName("AUTHOR")
    for author in authors:
        output.append(author + '\n')

    return ''.join(output)

def write_elements_to_archive(authors: str, path: str) -> None:
    """Given a string with elements, write it to an archive
    Args:
        authors (str): The elements to be written in the path
        path (str): The path where the elements will be written
    """
    with open(path, 'w') as output:
        output.write(authors)

if __name__ == '__main__':
    authors = extract_authors_from_xml(INPUT_PATH)
    write_elements_to_archive(authors, OUTPUT_PATH)