import html.parser


# Method to clean xml tags with unwanted codes or symbols
def clean_xml_tags(text):
    decodedContent = html.unescape(text)
    decodedContent = decodedContent.replace(" & ", " ")
    decodedContent = decodedContent.replace("&", "")
    decodedContent = decodedContent.replace("<>", " ")
    decodedContent = decodedContent.replace("&lt;", " ")
    decodedContent = decodedContent.replace("&gt;", " ")
    return decodedContent
