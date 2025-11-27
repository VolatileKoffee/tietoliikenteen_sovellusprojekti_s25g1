import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import logging

logger = logging.getLogger(__name__)


def prepare_data():
    measurementData = pd.read_csv("ml_analysis/data/measurementdata.csv")
    measurementData.drop(['time' , 'sensor_orientation'],axis= 1 , inplace=True)

    datavalues = measurementData[['sensor_x','sensor_y', 'sensor_z']].values
    # numberOfRows = data.shape[0]
    # print(f"Rows: {numberOfRows}")
    print(f"Shape: {datavalues.shape}\nMin: {datavalues.min()}\nMax: {datavalues.max()}")

    return datavalues


def assign_centroids(k, data):
    indices = np.random.choice(data.shape[0], k, replace=False)
    centroids = data[indices]
    print(f"centroids: {centroids}")
    return centroids

def datapoint_distances(p1,p2):
    return np.linalg.norm(p1 - p2)
    

if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    data = prepare_data()
    centroids = assign_centroids(6, data)
    running = True

    while running:
        cumCentWinCounterList = [0,0,0,0,0,0]
        cumList = np.zeros(centroids.shape)
        for x in data:
            comparison = float("inf") # original 3000
            counter = 0

            for i in centroids:
                tempDistance = datapoint_distances(x,i)

                if tempDistance < comparison:
                    comparison = tempDistance
                    closestcentroid = counter
                counter += 1
            
            cumList[closestcentroid] += x
            cumCentWinCounterList[closestcentroid] += 1
            # match closestcentroid:
            #     case 0:
            #         cumCentWinCounterList[0] += 1
            #     case 1:
            #         cumCentWinCounterList[1] += 1
            #     case 2:
            #         cumCentWinCounterList[2] += 1
            #     case 3:
            #         cumCentWinCounterList[3] += 1
            #     case 4:
            #         cumCentWinCounterList[4] += 1
            #     case 5:
            #         cumCentWinCounterList[5] += 1     
                    


        print(f"Cumulative list: {cumList}")
        print(f"Centroid win counts: {cumCentWinCounterList}")
        print(f"New place for centroid: {cumList[0] / cumCentWinCounterList[0]}")

        oldcentroids = centroids.copy() # copy prevents "linking" from happening
        for i in range(len(centroids)):
            if cumCentWinCounterList[i] == 0: # from 100 to 0
                centroids[i] = assign_centroids(1,data)
                print(centroids[i])

            else:
                centroids[i]= cumList[i] / cumCentWinCounterList[i]

        # MOVED LINES BELOW ONE STEP "BACK" OUT OF FOR-LOOP

        # difference_arr = (100-((oldcentroids.all() / centroids.all()) * 100))
        # if (difference_arr <= 10): # percentile <=threshold
        #     print(f"false, stopping")
        #     running = False

        # checking the convergence of centroids
        if np.allclose(centroids, oldcentroids, atol=1e-3):
            logger.info(f"Stopping...")
            running = False

        # iteration check? iteration += 1 if iteration > 100: running=False

        print(f"updated centroids:\n{centroids}")
        print(f"win counter {cumCentWinCounterList}")

    logger.info(f"Final centroids:\n{centroids}")

    # calculating total_error ?
    
        

# Finding the distance between datapoints (Euclidean distance)
# def euclidean_distance(p1, p2):
#     result = np.sqrt(np.sum((p1-p2)**2)) # TAI np.linalg.norm(x1 - x2)
#     print(f"result is {result}")
#     return result


# ---- Plotting ---- #
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot cluster centers
# for i in clusters:
#     center = clusters[i]['center']
#     ax.scatter(center[0], center[1], center[2], marker='*', c='red', s=200)

ax.scatter(data[:,0], data[:,1], data[:,2], c = 'red', alpha=0.1)
# for i in clusters:
#     center = clusters[i]['center']
#     ax.scatter(center[0],center[1], center[2],marker = '^',c = 'red')
ax.scatter(centroids[:,0], centroids[:,1], centroids[:,2], c = 'blue', marker='*', alpha=1, s=1000)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.grid(True)
plt.show()
