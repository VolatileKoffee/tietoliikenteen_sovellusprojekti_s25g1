import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

measurementData = pd.read_csv("ml_analysis/data/measurementdata.csv")
measurementData.drop(['time' , 'sensor_orientation'],axis= 1 , inplace=True)


# Creating initial random spots 
k = 6
clusters = {}
np.random.seed(23)
data = measurementData[['sensor_x','sensor_y', 'sensor_z']].values
print(f"{data.shape}")
print(f"Min: {data.min()}")
print(f"Max: {data.max()}")

# Finding the distance between datapoints
def distance(p1, p2):
    result = np.sqrt(np.sum((p1-p2)**2))
    print(f"result is {result}")
    return result


def assign_clusters(X, clusters):
    for idx in range(X.shape[0]):
        dist = []
        
        curr_x = X[idx]
        
        for i in range(k):
            dis = distance(curr_x,clusters[i]['center'])
            dist.append(dis)
        curr_cluster = np.argmin(dist)
        clusters[curr_cluster]['points'].append(curr_x)
    return clusters


def update_clusters(X, clusters):
    for i in range(k):
        points = np.array(clusters[i]['points'])
        if points.shape[0] > 0:
            new_center = points.mean(axis =0)
            clusters[i]['center'] = new_center
            
            clusters[i]['points'] = []
    return clusters


def pred_cluster(X, clusters):
    pred = []
    for i in range(X.shape[0]):
        dist = []
        for j in range(k):
            dist.append(distance(X[i],clusters[j]['center']))
        pred.append(np.argmin(dist))
    return pred   


data_min = data.min(axis=0)
data_max = data.max(axis=0)

for idx in range(k):
    center = data_min + np.random.random(data.shape[1]) * (data_max-data_min)    # creates a 3D center
    cluster = {
        'center': center,
        'points': []
    }
    clusters[idx] = cluster

clusters = assign_clusters(data, clusters)
clusters = update_clusters(data, clusters)
pred = pred_cluster(data, clusters)



# ---- Plotting ---- #
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot dataset points
#ax.scatter(data[:, 0], data[:, 1], data[:, 2])

# Plot cluster centers
"""for i in clusters:
    center = clusters[i]['center']
    ax.scatter(center[0], center[1], center[2],
               marker='*', c='red', s=200)
"""
ax.scatter(data[:,0],data[:,1], data[:, 2],c = pred)
for i in clusters:
    center = clusters[i]['center']
    ax.scatter(center[0],center[1], center[2],marker = '^',c = 'red')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.grid(True)
plt.show()

