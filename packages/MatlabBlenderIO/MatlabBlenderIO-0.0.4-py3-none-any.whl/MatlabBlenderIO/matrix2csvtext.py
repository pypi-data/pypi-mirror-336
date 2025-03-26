import numpy as np
import math

def matrix2csvtext(mat,*args, **kwargs):
    # Converts a matrix to text that can be written to a .csv file, encoding dimension-information based on the number of ",".
    mat = np.array(mat)
    starting_delimiter    = kwargs.get('starting_delimiter', None)
    if starting_delimiter == None: starting_delimiter = ","

    text               = ""
    dimensions         = mat.ndim
    dimension_lenghts  = list(mat.shape)
    number_of_elements = mat.size
    flatmat            = mat.reshape(number_of_elements, 1)

    denominator_multiplier = [1]+dimension_lenghts

    for index in range(1,number_of_elements+1):
        text += str(float(flatmat[index-1][0]))

        if index != number_of_elements:
            text += starting_delimiter
            for dim in range(2,dimensions+1):
                if ((index)%(dimension_lenghts[dim-1]*math.prod(denominator_multiplier[:dim-1])) ) == 0: text += ","
            for dim in range(2,dimensions+1):
                if ((index)%(dimension_lenghts[dim-1]*math.prod(denominator_multiplier[:dim-1])) ) == 0: text += "\n"

    return text



def matrix2csvtext_demo():
    print(matrix2csvtext(np.array(  ((1,2,3),(4,5,6),(7,8,9))  )))
    print(matrix2csvtext(np.array(  (((1,2,3)),((4,5,6)),((7,8,9)))  )))
    print(matrix2csvtext(np.array(  (1,2,3)  )))
    print(matrix2csvtext(np.array(  (1)  )))
    print(matrix2csvtext(np.array(  (((1,2),(3,4)),((5,6),(7,8)))  )))
    print(matrix2csvtext(np.array(  ((1,2,3),(4,5,6),(7,8,9))  ), starting_delimiter = ",,"))
    print(matrix2csvtext(np.array(  (((1,2,3)),((4,5,6)),((7,8,9)))  ), starting_delimiter = ",,,"))
    print(matrix2csvtext(np.array(  (1,2,3)  ), starting_delimiter = ",,,,"))
    print(matrix2csvtext(np.array(  (1)  ), starting_delimiter = ",,,,,"))
    print(matrix2csvtext(np.array(  (((1,2),(3,4)),((5,6),(7,8)))  ), ","))

#matrix2csvtext_demo()