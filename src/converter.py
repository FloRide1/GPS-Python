########################################
#
# Author: Florian FloRide Reimat
# Github: https://github.com/FloRide1/GPS-Python 
# About: This file list all conversion function
#
#########################################

import math
import colorsys

# Constants:
KNOT_TO_KM_H = 1.852001
RADIUS_OF_EARTH_IN_METERS = 6371009
DEGREE_TO_RADIANS = math.pi / 180

# Functions
def convert_frame_to_KML(frame: dict):
    """
    Convert parsed frames into "KML" data type (for my program)

        Parameters: 
            frame (dict): The parse frame data in a dict (see parser.py for better understanding)

        Returns: 
           Returns an dict with all the KML data for UI
    """
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
        print("[ERROR] An error occurred during conversion in KML format")
        return -1



def convert_GGA_to_KML(gga_frame: dict):
    """
    Convert GGA frame into "KML" data type

        Parameters: 
            frame (dict): The parse GGA frame in a dict (see parser.py for better understanding)

        Returns: 
           Returns an dict with all the KML data for UI
    """
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
                'type'      : "position", 
                'longitude' : longitude,
                'latitude'  : latitude,
                'altitude'  : gga_frame['altitude'] + 15 # The + 15 is just for avoid hidden point in ground
            }
            return kml_frame

        else:
            print("[ERROR] This is not an GGA frame")
            return -1
    except:
        print("[ERROR] The conversion between this GGA frame and KML is Impossible")
        return -1

def convert_VTG_to_KML(vtg_frame):
    """
    Convert VTG frame into "KML" data type

        Parameters: 
            frame (dict): The parse VTG frame in a dict (see parser.py for better understanding)

        Returns: 
           Returns an dict with all the KML data for UI
    """
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
        print("[ERROR] The conversion between this VTG frame and KML is Impossible")
        return -1

def convert_RMC_to_KML(rmc_frame):
    """
    Convert RMC frame into "KML" data type

        Parameters: 
            frame (dict): The parse RMC frame in a dict (see parser.py for better understanding)

        Returns: 
           Returns an dict with all the KML data for UI
    """
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
        print("[ERROR] The conversion between this RMC frame and KML is Impossible")
        return -1


def speed_to_hue(speed: float, min_speed: float = 0, max_speed: float = 100, min_hue: int = 140, max_hue: int = 0) -> float:
    """
    Convert a speed to a Hue value (in HSV color format) for progressive color changements over speed
    It just work like a linear function:
    [min_speed km/h; max_speed km/h] -> [min_hue; max_hue] (For HSV system)  

        Parameters:
            speed       (float): The actual speed
            min_speed   (float): The minimal speed expected
            max_speed   (float): The maximal speed expected
            min_hue     (int)  : The minimal speed hue value
            max_hue     (int)  : The maximal speed hue value

        Returns:
            It return the hue value associate with that speed
    """
    slope = (max_hue - min_hue) / (max_speed - min_speed)
    y_intercept = min_hue - (min_speed * slope) 
    hue = (slope * speed) + y_intercept 
    return hue

def convert_color_KML (hue: float, sat: float = 100, value: float = 100) -> str:
    """
    Convert a HSV value into the KML standard color format:
        AABBGGRR:
            - AA: Alpha value in (lowercase) Hex
            - BB: Blue  value in (lowercase) Hex 
            - GG: Green value in (lowercase) Hex 
            - RR: Red   value in (lowercase) Hex 

        Parameters:
            hue   (float): The hue value of the color
            sat   (float): The saturation value of the color
            value (float): The value of the color (HSV)

        Returns:
            An string containing the color in the KML format
    """
    hue /= 360
    sat /= 100
    value /= 100
    red, green, blue = colorsys.hsv_to_rgb(hue, sat, value)    
    red     = int(255 * red)
    green   = int(255 * green)
    blue    = int(255 * blue)
    kml_color = "ff{b:02x}{g:02x}{r:02x}".format(b=blue, g=green, r=red)
    return kml_color 

def calculate_dist_for_polar_coordinates(latitude_a: float, longitude_a: float, latitude_b: float, longitude_b: float) -> float:
    """
    Calculate and return the distance between 2 geographic coordinate points using 
    Harvesine Formula (en.wikipedia.org/wiki/Haversine_formula)
    
        Parameters:
            latitude_a  (float): The latitude  of point A in degree 
            longitude_a (float): The longitude of point A in degree 
            latitude_b  (float): The latitude  of point B in degree 
            longitude_b (float): The longitude of point B in degree 

        Returns:
        The distance between point A and B in meters (m)
    """
    lat_a = latitude_a  * DEGREE_TO_RADIANS
    lon_a = longitude_a * DEGREE_TO_RADIANS
    lat_b = latitude_b  * DEGREE_TO_RADIANS
    lon_b = longitude_b * DEGREE_TO_RADIANS
    
    a = math.sin((lat_b - lat_a) / 2) ** 2 + math.cos(lat_a) * math.cos(lat_b) * math.sin((lon_b - lon_a) / 2) ** 2
    distance = 2 * RADIUS_OF_EARTH_IN_METERS * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return distance

