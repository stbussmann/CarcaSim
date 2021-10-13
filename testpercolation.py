######################################
#### percolation test program     ####
#### by Stephan Bussmann          ####
######################################


import sys
import numpy as np
import stationarymodel as model
import multiprocessing

#This method creates a number of models and counts how many of them percolate
def test_percolation(iterations, WINDOW_WIDTH, WINDOW_HEIGHT, POINT_INTENSITY, COMM_RADIUS):

    result = 0

    for k in range(iterations):

        Z = model.BooleanModel(WINDOW_WIDTH, WINDOW_HEIGHT, POINT_INTENSITY, COMM_RADIUS)
        if Z.percolates():
            result+=1

    return result

#This method distributes iterations over all available CPUs
def multicore_test_percolation(ITERATIONS, WINDOW_WIDTH, WINDOW_HEIGHT, POINT_INTENSITY, COMM_RADIUS):

    cpu_count = multiprocessing.cpu_count()
    myPool = multiprocessing.Pool(cpu_count)

    iterations_per_cpu = int(ITERATIONS/cpu_count)

    result_objects = []
    for cpu in range(cpu_count):

        result_objects.append(myPool.apply_async(test_percolation, (iterations_per_cpu,WINDOW_WIDTH, WINDOW_HEIGHT, POINT_INTENSITY, COMM_RADIUS,)))

    myPool.close()
    myPool.join()

    number_of_percolating_models = 0

    for number in result_objects:
        number_of_percolating_models += number.get()

    return number_of_percolating_models

def draw_model(WINDOW_WIDTH, WINDOW_HEIGHT, POINT_INTENSITY, COMM_RADIUS):

    Z = model.BooleanModel(WINDOW_WIDTH, WINDOW_HEIGHT, POINT_INTENSITY, COMM_RADIUS)
    print('Drawn '+str(Z.number_of_points)+' nodes and '+str(len(Z.set_of_connections))+' connections.')
    Z.draw()

#########################################################
####  INPUT BLOCK                                    ####
#########################################################

input_ok = False
while input_ok==False:
    try:
        WINDOW_HEIGHT = int(input("Height of observation window:"))
        if WINDOW_HEIGHT <= 0: raise ValueError
        input_ok=True
    except ValueError:
        print("Has to be an integer greater than zero!")
        input_ok=False

WINDOW_WIDTH  = 3*WINDOW_HEIGHT

input_ok = False
while input_ok==False:
    try:
        POINT_INTENSITY = float(input("Intensity of point process:"))
        input_ok=True
    except ValueError:
        print("Has to be a float greater than zero!")
        input_ok=False

input_ok = False
while input_ok==False:
    try:
        COMM_RADIUS = float(input("Communication radius of nodes:"))
        input_ok=True
    except ValueError:
        print("Has to be a float greater than zero!")
        input_ok=False

if 'test' in sys.argv:
    input_ok = False
    while input_ok==False:
        try:
            ITERATIONS = int(input("Number of simulations to run:"))
            input_ok=True
        except ValueError:
            print("Has to be an integer greater than zero!")
            input_ok=False

print()
print("***********************WORKING***************************")
print()

if 'draw' in sys.argv:
     draw_model(WINDOW_WIDTH, WINDOW_HEIGHT, POINT_INTENSITY, COMM_RADIUS)

if 'test' in sys.argv:
    n = multicore_test_percolation(ITERATIONS, WINDOW_WIDTH, WINDOW_HEIGHT, POINT_INTENSITY, COMM_RADIUS)
    print('Out of '+str(ITERATIONS)+' tested models '+str(n)+' did percolate.')
    print('Estimated percolation probability: '+ str(round(n/ITERATIONS, 2)))
    print()
