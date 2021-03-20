
def get_kml_data(coordinates):
    xml_line = get_kml_xml_line()
    kml_placeholder = get_placeholder_kml() 
    name_line = get_name_line()
    description_line = get_description_line()
    style_line = get_style_line()
    
    kml_final_line = []
    kml_final_line.append(xml_line)
    kml_final_line.append(kml_placeholder['begin'])

    kml_final_line.append(name_line)
    kml_final_line.append(description_line)
    kml_final_line.append(style_line)

    kml_final_line.append(kml_placeholder['end'])
    kml_file = "\n".join(kml_final_line)
        
    return kml_file
    

def get_kml_xml_line(version = 1.0, encoding = "UTF-8"):
    line = "<?xml version=\"{vrsn:.1f}\" encoding=\"{encd}\"?>".format(
        vrsn = version,
        encd = encoding
    )
    return line

def get_placeholder_kml(xmlns = "http://earth.google.com/kml/2.1",indent_lvl = 8):
    begin = "<kml xmlns=\"{xmlns_place}\">\n{indent}<Document>".format(
        indent = indent_lvl * " ",
        xmlns_place = xmlns
    )
    end = "{indent}</Document>\n</kml>".format(indent= indent_lvl * " ")
    placeholder = {
        'begin': begin,
        'end': end
    } 
    return placeholder

def get_name_line(name = "Paths", indent_lvl = 16):
    line = "{indent}<name>{nme}</name>".format(
        indent = indent_lvl * " ",
        nme = name
    )
    return line

def get_description_line(description = "My Journey", indent_lvl = 16):
    line = "{indent}<description>{dscp}</description>".format(
        indent = indent_lvl * " ",
        dscp = description 
    )
    return line

def get_style_line(name_id = "yellowLineGreenPoly", line_color = 2130771967, line_width = 4, 
    poly_color = 2130771967, indent_base = 16, indent_lvl = 8):
    b_Style_line = "{indent}<Style id=\"{n_id}\">".format(indent = indent_base * " ", n_id = name_id)
    b_Line_line = "{indent}<LineStyle>".format(indent = (indent_base + 1 * indent_lvl) * " ")
    line_color_line = "{indent}<color>{l_color:8x}</color>".format(indent = (indent_base + 2 * indent_lvl) * " ", l_color = line_color)
    line_width_line = "{indent}<width>{l_width}</width>".format(indent = (indent_base + 2 * indent_lvl) * " ", l_width = line_width)
    e_Line_line = "{indent}</LineStyle>".format(indent = (indent_base + 1 * indent_lvl) * " ")
    poly_color_line = "{indent}<color>{l_color:8x}</color>".format(indent = (indent_base + 2 * indent_lvl) * " ", l_color = poly_color)
    b_Poly_line = "{indent}<PolyStyle>".format(indent = (indent_base + 1 * indent_lvl) * " ")
    e_Poly_line = "{indent}</PolyStyle>".format(indent = (indent_base + 1 * indent_lvl) * " ")
    e_Style_line = "{indent}</Style>".format(indent = indent_base * " ")

    global_line = []
    global_line.append(b_Style_line)
    global_line.append(b_Line_line)
    global_line.append(line_color_line)
    global_line.append(line_width_line)
    global_line.append(e_Line_line)
    global_line.append(b_Poly_line)
    global_line.append(poly_color_line)
    global_line.append(e_Poly_line)
    global_line.append(e_Style_line)

    global_line = "\n".join(global_line)

    return global_line

