########################################
#
# Author: Florian FloRide Reimat
# Github: https://github.com/FloRide1/GPS-Python 
# About: This file list all parsing function for .nmea frame
# Licence: GNU 3
#
#########################################

def parse_file(file_data: str):
    """
    Split each line of .nmea file and parse all frame inside of them
    
        Parameters:
            file_data (string): The all file content with all frame separated by line

        Returns: 
            An array of dict which contain all the parsed data
    """
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
    

def parse_frame(data: str, line: int):
    """
    Select and redirect frame by the type (Ex: GGA, VTG, etc...) for parsing it.

        Parameters:
            data (string): The frame string unparsed
            line    (int): The data line number 

        Returns:
            The data dict parse.
    """
    try:
        parse_data = data.split(",")
        # Data Form: [type, X, X, ...]

        typeOfFrame = parse_data[0][3:] # Take only the X: $GPXXX
        if   (typeOfFrame == "GGA"):
            frame_data = parse_GGA_frame(parse_data)
        elif (typeOfFrame == "VTG"):
            frame_data = parse_VTG_frame(parse_data)
        elif (typeOfFrame == "RMC"):
            frame_data = parse_RMC_frame(parse_data)
        else:
            # Type is unhandle
            frame_data = 0
        return frame_data
    except:
        print("[ERROR] Parsing had failed - line: " + str(line))
        return -1

def parse_GGA_frame(parse_data: list[str]):
    """ 
    Parse GGA frame and return a dict with all the data

        Parameters:
            parse_data (list[string]): The frame array with all data in string

        Returns:
            The dict of the GGA frame
    """
    try:
        typeOfFrame = parse_data[0][3:] 
        if typeOfFrame == "GGA":
            frame_data = {
                'type'          : parse_data[0][3:],
                'time'          : float(parse_data[1]),
                'latitude'      : float(parse_data[2]),
                'north_south'   : parse_data[3],
                'longitude'     : float(parse_data[4]),
                'est_west'      : parse_data[5],
                'quality'       : float(parse_data[6]),
                'numb_of_sats'  : parse_data[7],
                'HDOP'          : parse_data[8],
                'altitude'      : float(parse_data[9]),
                'units'         : parse_data[10]
            }
            return frame_data
        else:
            print("[ERROR] This frame is not an GGA frame")
            return -1
    except:
        print("[ERROR] This GGA frame is not correctly formated: ")
        print(parse_data)
        return -1
    
def parse_VTG_frame(parse_data: list[str]):
    """ 
    Parse VTG frame and return a dict with all the data

        Parameters:
            parse_data (list[string]): The frame array with all data in string

        Returns:
            The dict of the VTG frame
    """
    try:
        typeOfFrame = parse_data[0][3:]
        if typeOfFrame == "VTG":
           frame_data = {
                'type' : typeOfFrame,
                'speed_km' : float(parse_data[7])
            }
           return frame_data
        else:
            print("[ERROR] This frame is not an VTG frame")
    except:
        print("[ERROR] This VTG frame is not correctly formated: ")
        print(parse_data)
        return -1

def parse_RMC_frame(parse_data: list[str]):
    """ 
    Parse RMC frame and return a dict with all the data

        Parameters:
            parse_data (list[string]): The frame array with all data in string

        Returns:
            The dict of the RMC frame
    """
    try:
        typeOfFrame = parse_data[0][3:]
        if typeOfFrame == "RMC":
           frame_data = {
                'type' : typeOfFrame,
                'speed_knot' : float(parse_data[7])
            }
           return frame_data
        else:
            print("[ERROR] This frame is not an RMC frame")
    except:
        print("[ERROR] This RMC frame is not correctly formated: ")
        print(parse_data)
        return -1

def parse_ZDA_frame(parse_data: list[str]):
    """ 
    Parse ZDA frame and return a dict with all the data

        Parameters:
            parse_data (list[string]): The frame array with all data in string

        Returns:
            The dict of the ZDA frame
    """
    try:
        typeOfFrame = parse_data[0][3:]
        if typeOfFrame == "ZDA":
           frame_data = {
                'type' : typeOfFrame,
                'utc' : parse_data[1],
                'day' : int(parse_data[2]),
                'month' : int (parse_data[3]),
                'year' : int(parse_data[4]),
            }
           return frame_data
        else:
            print("[ERROR] This frame is not an ZDA frame")
    except:
        print("[ERROR] This ZDA frame is not correctly formated: ")
        print(parse_data)
        return -1

