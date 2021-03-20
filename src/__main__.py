
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
            raise TypeError("Parse fail")
        print("[OK] Data is Correctly Parse")
    except:
        print("[ERROR] Data can't be Parse")
        return -1

    print("[OK] Main End")

def parse_file(file_data):
    try:
        data_list = file_data.split("\n") # Split Each Line of Data
        print("[OK] File is correctly parsed")
        correct_data = []
        for i in range(len(data_list)):
            data = data_list[i]
            frame_data = parse_frame(data,i + 1)
            if frame_data == -1:
                raise TypeError("Parse failed")
            correct_data.append(frame_data)
        return correct_data
    except:
        print("[ERROR] Parsing File is impossible")
        return -1
    

def parse_frame(data, line):
    try:
        parse_data = data.split(",")
        # Data Form: [type, ]
        typeOfFrame = parse_data[0][3:] # Take only take the X: $GPXXX
        if (typeOfFrame == "GGA"):
            frame_data = {
                'time'            : int(parse_data[1]),
                'latitude'        : float(parse_data[2]),
                'NorthOrSouth'    : parse_data[3],
                'longitude'       : float(parse_data[4]),
                'EstOrWest'       : parse_data[5],
                'quality'         : float(parse_data[6])
            }
        else:
            frame_data = 0
        return frame_data
    except:
        print("[ERROR] Parsing had failed - line: " + str(line))
        return -1


if __name__ == "__main__":
    init()
    main()

