
def get_kml_data(coordinates):
    xml_line = get_kml_xml_line()
    kml_placeholder = get_placeholder_kml() 
    
    kml_file = "\n".join([xml_line, kml_placeholder['begin'], "Test",
        kml_placeholder['end']])
    return kml_file
    

def get_kml_xml_line(version = 1.0, encoding = "UTF-8"):
    line = "<?xml version=\"{vrsn:.1f}\" encoding=\"{encd}\"?>".format(
        vrsn = version,
        encd = encoding
    )
    return line

def get_placeholder_kml(xmlns = "http://earth.google.com/kml/2.1"):
    begin = "<kml xmlns=\"{xmlns_place}\">\n    <Document>".format(
        xmlns_place=xmlns
    )
    end = "    </Document>\n</kml>"
    placeholder = {
        'begin': begin,
        'end': end
    } 
    return placeholder
