from parser import *
from converter import *
from kml import * 

DATA_PATH = "./data/"
DATA_FILE = "balade_gps.txt"
OUTPUT_PATH = "./output/"
OUTPUT_FILE = "kml_output.kml"

def init():
    print("[OK] Init Begin")
    print("[OK] File Path: " + DATA_PATH)
    print("[OK] File Name: " + DATA_FILE)
    print("[OK] Output Path: " + OUTPUT_PATH)
    print("[OK] Output File: " + OUTPUT_FILE)
    print("[OK] Init End")

def main():
    print("[OK] Main Begin")
    try: 
        file_object = open(DATA_PATH + DATA_FILE, 'r')
        file_data = file_object.read()
        print("[OK] File is Open")
    except:
        print("[ERROR] File didn't Open")
        return -1
    try:
        data = parse_file(file_data)
        if data == -1:
            raise TypeError("Parse failed")
        print("[OK] Data is correctly parsed")
    except:
        print("[ERROR] Data can't be parsed")
        return -1
    try:
        kml_data = []
        for d in data:
            kml_d = convert_frame_to_KML(d)
            if (kml_d == -1):
                raise TypeError("Conversion failed")
            elif kml_d != -2:
                kml_data.append(kml_d) 
        print("[OK] Conversion in KML Success")
    except:
        print("[ERROR] Convertion in KML failed")
        return -1
    try:
        kml_file = get_kml_file_data(kml_data) 
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

    print("[OK] Main End")

if __name__ == "__main__":
    init()
    main()

