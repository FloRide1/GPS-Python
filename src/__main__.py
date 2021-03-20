from parser import *
from converter import *
from kml import * 

DATA_PATH = "./data/"
DATA_FILE = "data_example.txt"


def init():
    print("[OK] Init Begin")
    print("[OK] File Path: " + DATA_PATH)
    print("[OK] File Name: " + DATA_FILE)
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
    print(get_kml_data("1"))

    print("[OK] Main End")

if __name__ == "__main__":
    init()
    main()

