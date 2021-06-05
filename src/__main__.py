########################################
#
# Author: Florian FloRide Reimat
# Github: https://github.com/FloRide1/GPS-Python 
# About: This file is the main file of the project
# Licence: GNU 3
#########################################

import math
import parser_functions as parser
import converter
import kml

CONFINEMENT_RADIUS = 3000

DATA_PATH = "./data/"
DATA_FILE = "balade_gps.txt"
OUTPUT_PATH = "./output/"
OUTPUT_FILE = "kml_output.kml"

def init():
    """
    Init of the Main Program
    """
    print("[OK] Init Begin")
    print("[OK] File Path: " + DATA_PATH)
    print("[OK] File Name: " + DATA_FILE)
    print("[OK] Output Path: " + OUTPUT_PATH)
    print("[OK] Output File: " + OUTPUT_FILE)
    print("[OK] Init End")

def main():
    """
    Main Loop of Program
    """
    print("[OK] Main Begin")
    try: 
        file_object = open(DATA_PATH + DATA_FILE, 'r')
        file_data = file_object.read()
        print("[OK] File is Open")
    except:
        print("[ERROR] File didn't Open")
        return -1
    try:
        data = parser.parse_file(file_data)
        if data == -1:
            raise TypeError("Parse failed")
        print("[OK] Data is correctly parsed")
    except:
        print("[ERROR] Data can't be parsed")
        return -1
    try:
        kml_data = []
        for d in data:
            kml_d = converter.convert_frame_to_KML(d)
            if (kml_d == -1):
                raise TypeError("Conversion failed")
            elif kml_d != -2:
                kml_data.append(kml_d) 
        print("[OK] Conversion in KML Success")
    except:
        print("[ERROR] Conversion in KML failed")
        return -1
    try:
        kml_file = kml.get_kml_file_data(kml_data) 
        if kml_file == -1:
            raise TypeError("KML Can't be generate")
        print("[OK] The KML file data is generate")
    except:
        print("[ERROR] The KML file data can't be generate") 
        return -1
    try:
        output_file = open(OUTPUT_PATH + OUTPUT_FILE, 'w')
        output_file.write(kml_file)
        print("[OK] Output File is done")
    except:
        print("[ERROR] Output File can't be generated")
        return -1
    try:
        # Calculate Distance
        house_position = -1
        max_distance = 0
        for pos_and_speed_data in kml_data:
            if (pos_and_speed_data['type'] == "position"):
                if house_position == -1:
                    house_position = pos_and_speed_data
                else:
                    latitude_a  = house_position['latitude']
                    longitude_a = house_position['longitude']
                    latitude_b  = pos_and_speed_data['latitude']
                    longitude_b = pos_and_speed_data['longitude']
                    distance = converter.calculate_dist_for_polar_coordinates(latitude_a, longitude_a, latitude_b, longitude_b)
                    if (distance > max_distance):
                        max_distance = distance
        print("[OK] Max distance: " + str(math.floor(max_distance)) + "m")
        if (max_distance < CONFINEMENT_RADIUS):
            print("[OK] Containment is respected")
        else:
            print("[ERROR] Containment is not respected: The police were called")
    except:
        print("[ERROR] Max distance can't be calculated")
        return -1
    print("[OK] Main End")

if __name__ == "__main__":
    init()
    main()

