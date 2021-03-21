import colorsys

KNOT_TO_KM_H = 1.852001

def convert_frame_to_KML(frame):
    try:
        typeOfFrame = frame['type']
        if (typeOfFrame == "GGA"):
            if frame['quality'] != 0:
                return convert_GGA_to_KML(frame)
            else:
                return -2
        elif typeOfFrame == "VTG":
            return convert_VTG_to_KML(frame)
        elif typeOfFrame == "RMC":
            return convert_RMC_to_KML(frame)
        else:
            print("[ERROR] This frame format isn't handle: " + typeOfFrame)
            return -2
    except:
        print("[ERROR] An error occured during conversion in KML format")
        return -1



def convert_GGA_to_KML(gga_frame):
    try:
        if (gga_frame['type'] == "GGA"):
            longitude_GGA = str(gga_frame['longitude'])
            latitude_GGA  = str(gga_frame['latitude'])

            coeff_latitude = (-1,1) [gga_frame['north_south'] == "N"]
            coeff_longitude = (-1,1) [gga_frame['est_west']    == "E"]

            longitude_split = longitude_GGA.split(".")
            latitude_split  = latitude_GGA.split(".")

            longitude_degree = int(longitude_split[0][:-2])
            latitude_degree = int(latitude_split[0][:-2])

            longitude_minute = float(longitude_split[0][-2:] + "." + longitude_split[1])
            latitude_minute = float(latitude_split[0][-2:] + "." + latitude_split[1])

            longitude = (longitude_degree + longitude_minute / 60) * coeff_longitude
            latitude  = (latitude_degree + latitude_minute  / 60) * coeff_latitude

            kml_frame = {
                'type'      : "GGA",
                'longitude' : longitude,
                'latitude'  : latitude,
                'altitude'  : gga_frame['altitude'] + 15 # The + 15 is just for avoid hidden point in ground
            }
            return kml_frame

        else:
            print("[ERROR] This is not an GGA frame")
            return -1
    except:
        print("[ERROR] The conversion betweem this GGA frame and KML is Impossible")
        return -1

def convert_VTG_to_KML(vtg_frame):
    try:
        if (vtg_frame['type'] == "VTG"):
            speed = vtg_frame['speed_km'] 
            hue = speed_to_hue(speed)
            color = convert_color_KML(hue)
            kml_frame = {
                'type' : "speed",
                'speed': speed,
                'color': color
            }
            return kml_frame
        else:
            print("[ERROR] This is not an VTG frame")
            return -1
    except:
        print("[ERROR] The conversion betweem this VTG frame and KML is Impossible")
        return -1

def convert_RMC_to_KML(rmc_frame):
    try:
        if (rmc_frame['type'] == "RMC"):
            speed = rmc_frame['speed_knot']  * KNOT_TO_KM_H
            hue = speed_to_hue(speed)
            color = convert_color_KML(hue)
            kml_frame = {
                'type' : "speed",
                'speed': speed,
                'color': color
            }
            return kml_frame
        else:
            print("[ERROR] This is not an RMC frame")
            return -1
    except:
        print("[ERROR] The conversion betweem this RMC frame and KML is Impossible")
        return -1


def speed_to_hue(speed, min_speed = 0, max_speed = 100, min_hue = 140, max_hue = 0):
    # Conversion law [0km/h; 100km/h] -> [140;0] == [turquoise, red] (For HSV system)
    slope = (max_hue - min_hue) / (max_speed - min_speed)
    y_intercept = min_hue - (min_speed * slope) 
    hue = (slope * speed) + y_intercept 
    return hue

def convert_color_KML (hue , sat = 100, value = 100):
    hue /= 360
    sat /= 100
    value /= 100
    red, green, blue = colorsys.hsv_to_rgb(hue, sat, value)    
    red     = int(255 * red)
    green   = int(255 * green)
    blue    = int(255 * blue)
    kml_color = "ff{b:02x}{g:02x}{r:02x}".format(b=blue, g=green, r=red)
    return kml_color 


