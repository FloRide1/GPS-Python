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
            elif frame_data != 0:
                correct_data.append(frame_data)
        return correct_data
    except:
        print("[ERROR] Parsing File is impossible")
        return -1
    

def parse_frame(data, line):
    try:
        parse_data = data.split(",")
        # Data Form: [type, X, X, ...]
        typeOfFrame = parse_data[0][3:] # Take only the X: $GPXXX
        if (typeOfFrame == "GGA"):
            frame_data = parse_GGA_frame(parse_data)
        else:
            frame_data = 0
        return frame_data
    except:
        print("[ERROR] Parsing had failed - line: " + str(line))
        return -1

def parse_GGA_frame(parse_data):
    try:
        typeOfFrame = parse_data[0][3:] 
        if typeOfFrame == "GGA":
            frame_data = {
                'type'          : parse_data[0][3:],
                'time'          : int(parse_data[1]),
                'latitude'      : float(parse_data[2]),
                'north_south'   : parse_data[3],
                'longitude'     : float(parse_data[4]),
                'est_west'      : parse_data[5],
                'quality'       : float(parse_data[6]),
                'altitude'      : int(parse_data[7])
            }
            return frame_data
        else:
            print("[ERROR] This frame is not an GGA frame")
            return -1
    except:
        print("[ERROR] This GGA frame is not correctly formated")
        return -1
    
