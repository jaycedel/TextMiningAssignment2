from xml.etree  import ElementTree

testf = '<foo>&moo_1;</foo>'

parser = ElementTree.XMLParser()
parser.parser.UseForeignDTD(True)
parser.entity['moo_1'] = 'MOOOOO'

etree = ElementTree.ElementTree()

tree = etree.parse(testf, parser=parser)

for node in tree.iter('foo'):
    print (node.text)