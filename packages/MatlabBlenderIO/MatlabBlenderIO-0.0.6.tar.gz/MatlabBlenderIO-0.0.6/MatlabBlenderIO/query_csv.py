import numpy as np
from MatlabBlenderIO import csvtext2matrix
import csv


def query_csv(filepath, inquiry):
    # Querys .csv file for specific data.

    with open(filepath, mode='r') as file:
        data = file.read()
    
    data = data.replace("\n", "")
    data = data.replace("\n", "")
    data = data.split(",,,,,,")
    data = list(map(lambda element: element.split(",,,,,"), data))
    data = [list(filter(lambda item: item != '', element )) for element in data if type(element) is list]
    data = data[:-1]

    inquiry = data[0][0] + "." + inquiry
    full_inquiry = list(filter(lambda element: inquiry in element, data))
    if len(full_inquiry) == 0:
        print(inquiry)
        raise ValueError('File does not contain query.')
    index = data.index(full_inquiry[0])
    try:
        return csvtext2matrix(data[index][1])
    except:
        return data[index][1], 0


