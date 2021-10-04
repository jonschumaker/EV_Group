import numpy as np
#matrix is nX2 where columns represent
#height, speed
#rows represent height and speed after n seconds
def EV_energy_consumption(matrix, mass, air_resistance_coefficient,\
                          projected_area, rolling_resistance_coefficient):
    energy_consumed = 0
    for i in range(1, matrix.shape[0]):
        height_change = 0
        if matrix[i,0] > matrix[i-1,0]:
            height_change = matrix[i,0] - matrix[i-1,0]
        energy_consumed += mass*matrix[i,1]*(matrix[i,1] - matrix[i-1,1])\
        + 0.5*1.24*air_resistance_coefficient*projected_area*matrix[i,1]**3\
        + mass*9.8*height_change\
        + mass*rolling_resistance_coefficient*9.8*matrix[i,1]
    return energy_consumed

a = np.array([[1,55],[2,55],[3,55]])
EV_energy_consumption(a,1200,0.37,2.14,0.015)
