
def get_kml_file_data(coordinates, thresold = 1):
    try:
        xml_line = get_kml_xml_line()
        kml_placeholder = get_placeholder_kml() 
        name_line = get_name_line()
        description_line = get_description_line()
    
        kml_final_line = []
        kml_final_line.append(xml_line)
        kml_final_line.append(kml_placeholder['begin'])

        kml_final_line.append(name_line)
        kml_final_line.append(description_line)
        
        # print("\n".join(kml_final_line))
    
        placemark_speeds = get_placemark_content(coordinates, thresold)
        kml_final_line.append(placemark_speeds)

        kml_final_line.append(kml_placeholder['end'])
        kml_file = "\n".join(kml_final_line)
        
        return kml_file
    except:
        print("[ERROR] The KML file is broken")
        return -1
    

def get_placemark_content(coordinates, thresold):
    try:
        placemark_placeholder_lines = get_bracket_line("Placemark", 16) 
        lineString_line = get_bracket_line("LineString", 24)
        extrude_line = get_unique_line("extrude", 1, 32)
        tessellate_line = get_unique_line("tessellate", 1, 32)
        altitudeMode_line = get_unique_line("altitudeMode", "absolute", 32)
        coordinates_placeholder_lines = get_bracket_line("coordinates", 32)
        kml_line = []
        
        i = 0
        color = 0
        last_line = -1
        inPlaceHolder = False
        while color == 0:
            if (coordinates[i]['type'] == "speed"):
                speed = coordinates[i]['speed'] 
                color = coordinates[i]['color']
            i += 1
            if i >= len(coordinates):
                print("[ERROR] There is no color information (VTG || RMC) in this data")
                return -1

        for coords in coordinates:
            if (coords['type'] == "GGA"):
                if (not(inPlaceHolder)):
                    inPlaceHolder = True
                    kml_line.append(placemark_placeholder_lines['begin'])
                
                    style_line = get_style_line(color) 
                    kml_line.append(style_line)

                    kml_line.append(lineString_line['begin'])

                    kml_line.append(extrude_line)
                    kml_line.append(tessellate_line)
                    kml_line.append(altitudeMode_line)

                    kml_line.append(coordinates_placeholder_lines['begin'])
                    if (last_line != -1): 
                        kml_line.append(last_line)
    
                try: 
                    longitude = str(coords['longitude'])
                    latitude  = str(coords['latitude'])
                    altitude  = str(coords['altitude'])
                    last_line = 40 * " " + ",".join([longitude, latitude, altitude])
                    kml_line.append(last_line)
                except:
                    print("[ERROR] The coordinates can't be added in the KML file")
                    return -1
            elif (coords['type'] == "speed"):
                if (coords['speed'] < speed - thresold or coords['speed'] > speed + thresold):
                    speed = coords['speed']
                    color = coords['color']
                    inPlaceHolder = False
        
                    kml_line.append(coordinates_placeholder_lines['end'])
                    kml_line.append(lineString_line['end'])
                    kml_line.append(placemark_placeholder_lines['end'])
        if (inPlaceHolder):
            kml_line.append(coordinates_placeholder_lines['end'])
            kml_line.append(lineString_line['end'])
            kml_line.append(placemark_placeholder_lines['end'])
        kml_line = "\n".join(kml_line)
        return kml_line
    except:
        print("[ERROR] The PlaceHolder's KML line can't be generated")


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
    line = get_unique_line("name",name, indent_lvl)
    return line

def get_description_line(description = "My Journey", indent_lvl = 16):
    line = get_unique_line("description", description, indent_lvl)
    return line

def get_style_poly_line(name_id = "yellowLineGreenPoly", line_color = 2130771967, line_width = 4, 
    poly_color = 2130771967, indent_base = 16, indent_lvl = 8):
    b_Style_line = "{indent}<Style id=\"{n_id}\">".format(indent = indent_base * " ", n_id = name_id)
    e_Style_line = "{indent}</Style>".format(indent = indent_base * " ")

    Line_line = get_bracket_line("LineStyle", indent_base + indent_lvl)
    Poly_line = get_bracket_line("PolyStyle", indent_base + indent_lvl)

    line_color_line = get_unique_line("color", "{:8x}".format(line_color),indent_base + 2 * indent_lvl)
    poly_color_line = get_unique_line("color", "{:8x}".format(poly_color),indent_base + 2 * indent_lvl)
    line_width_line = get_unique_line("width", line_width,indent_base + 2 * indent_lvl)

    global_line = []
    global_line.append(b_Style_line)
    global_line.append(Line_line['begin'])
    global_line.append(line_color_line)
    global_line.append(line_width_line)
    global_line.append(Line_line['end'])
    global_line.append(Poly_line['begin'])
    global_line.append(poly_color_line)
    global_line.append(Poly_line['end'])
    global_line.append(e_Style_line)

    global_line = "\n".join(global_line)

    return global_line

def get_style_line(line_color , line_width = 8, indent_base = 24, indent_lvl = 8):
    Style_line = get_bracket_line("Style", indent_base)

    Line_line = get_bracket_line("LineStyle", indent_base + indent_lvl)

    line_color_line = get_unique_line("color", line_color,indent_base + 2 * indent_lvl)
    line_width_line = get_unique_line("width", line_width,indent_base + 2 * indent_lvl)

    global_line = []
    global_line.append(Style_line['begin'])
    global_line.append(Line_line['begin'])
    global_line.append(line_color_line)
    global_line.append(line_width_line)
    global_line.append(Line_line['end'])
    global_line.append(Style_line['end'])

    global_line = "\n".join(global_line)

    return global_line

def get_unique_line(name, value, indent):
    line = "{indent_b}<{nme}>{val}</{nme}>".format(indent_b = indent * " ", nme = name, val = value)
    return line

def get_bracket_line(name, indent):
    begin = "{indent_b}<{nme}>".format(indent_b=indent * " ", nme=name)
    end = "{indent_b}</{nme}>".format(indent_b=indent * " ", nme=name)
    line = {
        'begin': begin,
        'end': end
    }
    return line
