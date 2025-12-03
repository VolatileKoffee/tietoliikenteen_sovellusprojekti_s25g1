import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import logging

logger = logging.getLogger(__name__)


# 1. Read and process the data to datavalues-dataframe 
def prepare_data():
    measurementData = pd.read_csv("ml_analysis/data/measurementdata.csv")
    measurementData.drop(['time' , 'sensor_orientation'],axis= 1 , inplace=True)

    datavalues = measurementData[['sensor_x','sensor_y', 'sensor_z']].values
    # numberOfRows = data.shape[0]
    # print(f"Rows: {numberOfRows}")
    print(f"Shape: {datavalues.shape}\nMin: {datavalues.min()}\nMax: {datavalues.max()}")

    return datavalues

# 2. Assigning centroids
def assign_centroids(k, data):
    indices = np.random.choice(data.shape[0], k, replace=False)
    centroids = data[indices]
    print(f"centroids: {centroids}")
    return centroids


# Finding the distance between datapoints (Euclidean distance)
def datapoint_distances(p1,p2):
    return np.linalg.norm(p1 - p2)
    

# Sorts XYZ-values, formats values to C style and build the header file
def header_maker(final_centroids):
    logger.info(f"START: final_centroids:\n{final_centroids}\nfinal_centroids shape:{final_centroids.shape}")

    new_selection_order = [
    np.argmax(final_centroids[:,0]), # high x
    np.argmin(final_centroids[:,0]), # low x
    np.argmax(final_centroids[:,1]), # high y 
    np.argmin(final_centroids[:,1]), # low y
    np.argmax(final_centroids[:,2]), # high z
    np.argmin(final_centroids[:,2])  # low z
    ]
    
    sorted_centroids = final_centroids[new_selection_order] # applying the sort

    raw_c_rows = [f"{{{row[0]}, {row[1]}, {row[2]}}}" for row in sorted_centroids] # formats array to c style
    joined_c_rows = ",\n".join(raw_c_rows) # joins raw rows together

    logger.info(f"Centroids are sorted and joined:\n{joined_c_rows}")

    c_content = f"""#ifndef CENTROID_DATA_H
#define CENTROID_DATA_H

const int centroid_coords[6][3] = {{
{joined_c_rows}
}};

#endif // CENTROID_DATA_H
"""
    
    filename="./ml_analysis/centroid_data.h"
    try:
        with open(filename, "w") as f:
            f.write(c_content)
            logger.info(f"Write to {filename} was succesful.")
    except IOError as e:
        logger.info(f"Couldn't write to a file {filename}: {e}")


def plotting_results(data, centroids):
    # Plotting blops and centroids to 3D space
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(data[:,0], data[:,1], data[:,2], c = 'red', alpha=0.1)

    ax.scatter(centroids[:,0], centroids[:,1], centroids[:,2], c = 'blue', marker='*', alpha=1, s=1000)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.grid(True)
    plt.show()


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    data = prepare_data()
    centroids = assign_centroids(6, data)
    running = True

    while running:
        # Initializing a list for centroid's "won" datapoints
        cumCentWinCounterList = [0,0,0,0,0,0]
        # Initializing a list for cumulative point calculation (won datapoint coords adding)
        cumList = np.zeros(centroids.shape)

        for datapoint in data:
            comparison = float("inf")
            counter = 0 # keeping track of centroid allocation
            
            for c in centroids:
                tempDistance = datapoint_distances(datapoint,c)

                if tempDistance < comparison:
                    comparison = tempDistance
                    closestcentroid = counter
                counter += 1
            
            # Adding datapoint coords to cumulative list
            cumList[closestcentroid] += datapoint
            # Adding +1 to centroid 
            cumCentWinCounterList[closestcentroid] += 1   
                    

        # logger.info(f"Cumulative list: {cumList}")
        # logger.info(f"Centroid win counts: {cumCentWinCounterList}")
        # logger.info(f"New coords for centroid: {cumList[0] / cumCentWinCounterList[0]}")

        oldcentroids = centroids.copy() # copy prevents "linking" from happening
        
        for i in range(len(centroids)):
            # If centroid has 0 "won" datapoints, assign new random coords for it
            if cumCentWinCounterList[i] == 0:
                centroids[i] = assign_centroids(1,data) 
                print(centroids[i])
            else:
                # If 
                centroids[i] = cumList[i] / cumCentWinCounterList[i]


        # Checking the convergence of centroids
        # If new centroids coords have not changed enough, stopping the loop.
        if np.allclose(centroids, oldcentroids, atol=1e-3):
            logger.info(f"Stopping...")
            running = False

        # iteration check? iteration += 1 if iteration > 100: running=False

        logger.info(f"Updated centroids:\n{centroids}")
        logger.info(f"Win counts:{cumCentWinCounterList}")

    logger.info(f"Final centroids:\n{centroids}")
    # logger.info(f"Centroids type:{centroids.dtype}")

    # do we want to calculate total_error ?

    # Forming header file from latest centroids
    header_maker(centroids)
    plotting_results(data, centroids)
