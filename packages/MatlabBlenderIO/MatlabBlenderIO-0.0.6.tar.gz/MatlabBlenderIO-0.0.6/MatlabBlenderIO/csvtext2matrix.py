import numpy as np
import re
from itertools import groupby

def csvtext2matrix(text):
    text = str(text)
    text = text.replace("\n", "")
    if not "," in text:
        mat = np.array(float(text))
        dimension_lengths = 0
    else:

        # Find highest and lowest delimiters:
        highest_delimiter_number, lowest_delimiter_number = find_comma_sequences(text)
        highest_delimiter = highest_delimiter_number*","
        lowest_delimiter  = lowest_delimiter_number *","

        
        # Find the length of each dimension:
        dimensions         = highest_delimiter_number - lowest_delimiter_number+1
        dimension_lengths  = [0]*dimensions
        dimension_iterator = dimensions
        delimiter_iterator = highest_delimiter
        module             = 1

        while True:
            data_split_along_dim                     = text.split(delimiter_iterator)
            data_split_along_dim                     = list(filter( lambda x: x!="", data_split_along_dim ))
            dimension_lengths[dimension_iterator-1]  = int(len(data_split_along_dim)/module)
            module                                  *= dimension_lengths[dimension_iterator-1]

            if delimiter_iterator == lowest_delimiter:
                break
            else:
                delimiter_iterator  = delimiter_iterator[:-1]
                dimension_iterator -= 1

        # Making the matrix:
        flat_data = text.split(",")
        flat_data = list(filter( lambda x: x!="", flat_data ))
        flat_data = list(map(float, flat_data ))

        
        mat = np.array(flat_data)
        if dimensions > 1:
            mat = np.reshape(mat, dimension_lengths, 'F')

    return mat, dimension_lengths



def find_comma_sequences(text):
    comma_sequences = re.findall(r',+', text)
    if comma_sequences:
        longest  = max(len(seq) for seq in comma_sequences)
        smallest = min(len(seq) for seq in comma_sequences)
        return longest, smallest
    else:
        return 0, 0





def csvtext2matrix_demo():

    print(csvtext2matrix("0,0,0,,0,0,0,,,0,0,0,,0,0,0,,,0,0,0,,0,0,0"))
    print(csvtext2matrix("0,0,0,,0,0,0,,,0,0,0,,0,0,0"))
    print(csvtext2matrix("0,0,0,,0,0,0"))
    print(csvtext2matrix("0,1,3"))
    print(csvtext2matrix("0"))
    print(csvtext2matrix("0,1,0,,0,0,0,,,0,5,0,,8,0,0"))
    print(csvtext2matrix("0,,,1,,,2,,,4"))
    print(csvtext2matrix("0,,,,1,,,,2,,,,4"))
    testmat, testdims = csvtext2matrix("0,1,0,,0,0,0,,,0,5,0,,8,0,0")
    print(testmat[1][0][0])
    print(testmat[1][0][1])
    print(testmat[0][1][1])
    print(csvtext2matrix("0,1,0,0,0,0,,,0,5,0,8,0,0"))



csvtext2matrix_demo()