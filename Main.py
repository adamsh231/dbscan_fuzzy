# %%
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import csv
from sklearn import preprocessing
from collections import Counter

# %% Reading Data
fileOpen = open('baseball.csv')
readFile = csv.reader(fileOpen)
data = list(readFile)
position = []

for i in range(len(data)):
    position.append(data[i][2])

X = []
Y = []
Z = []

for i in range(len(data)):
    del data[i][:3]
    for j in range(len(data[0])):
        data[i][j] = float(data[i][j])
       
# min_max_scaler = preprocessing.MinMaxScaler()
# data = min_max_scaler.fit_transform(data)

# %% Visualization

for i in range(len(data)):
    X.append(data[i][0])
    Y.append(data[i][1])
    Z.append(data[i][2])

fig = plt.figure()
ax = plt.axes(projection="3d")

ax.scatter3D(X, Y, Z, c='blue')

ax.set_xlabel('Height')
ax.set_ylabel('Weight')
ax.set_zlabel('Age')

plt.show()

#%% DBSCAN Fuzzy Core
from FuzzyCore import dbScanCore, convertCluster, convertNoise, silhouette, labeling
C, M, N = dbScanCore(data, 5, 9, 1);
dataCluster = convertCluster(data, C)
noise = convertNoise(data, N)

#%% Result
hasil = []
k = []
v = []

for i in range(len(C)):
    hasil.append([])
    for j in range(len(C[i])):
        hasil[i].append(position[C[i][j]])

lbl = labeling(data, C, N)
score = silhouette(data, lbl)

print("Jumlah Cluster : " + str(len(dataCluster)))
print("Jumlah Noise : " + str(len(noise)))
print("Silhouette Score : " + str(score))

for i in range(len(dataCluster)):
    k.append(Counter(hasil[i]).keys()) # equals to list(set(words))
    v.append(Counter(hasil[i]).values()) # counts the elements' frequency
    print("=================")
    print("Cluster "+str(i)+" :")
    print("-----------------")
    print(k[i])
    print(v[i])
    print("=================")
    
#%% Visualization
fig = plt.figure()
ax = plt.axes(projection="3d")
color = ['r','g','b','c','m','y','yellow','darkviolet','magenta','olive']

for i in range(len(dataCluster)):
    X , Y , Z = [], [], []
    for j in range(len(dataCluster[i])):
        X.append(dataCluster[i][j][0])
        Y.append(dataCluster[i][j][1])
        Z.append(dataCluster[i][j][2])
    ax.scatter3D(X, Y, Z, c=color[i])

X , Y , Z = [], [], []  
for i in range(len(noise)):
    X.append(data[i][0])
    Y.append(data[i][1])
    Z.append(data[i][2])
ax.scatter3D(X, Y, Z, c='black')

ax.set_xlabel('Height')
ax.set_ylabel('Weight')
ax.set_zlabel('Age')

plt.show()
 
# %%
