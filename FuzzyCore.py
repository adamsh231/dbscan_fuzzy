# %%
import numpy as np
from scipy.spatial import distance
from sklearn import metrics

# %%
def silhouette(data, labels):
    return metrics.silhouette_score(data,labels)

def labeling(data, cluster, noise):
    label = [0 for i in range(len(data))]
    for i in range(len(cluster)):
        for j in range(len(cluster[i])):
            label[cluster[i][j]] = i
    for i in range(len(noise)):
        label[noise[i]] = -1
    return label

def eucDistance(p1, p2):
    return distance.euclidean(p1, p2)

def pts(p, data, eps):
    P = []
    for i in range(len(data)):
        if i == p:
            continue
        dist = eucDistance(data[p], data[i])
        if dist <= eps:
            P.append(i)
    return P

def regionPts(p, data, minPts, maxPts, eps):
    P = pts(p, data, eps)
    m = 0
    if (len(P)+1) > minPts:
        if (len(P)+1)  >= maxPts:
            m = 1
        else:
            m = ((len(P)+1)  - minPts) / (maxPts - minPts)
    return P, m         
                
def dbScanCore(data, minPts, maxPts, eps):
    marked = [0 for i in range(len(data))]
    noise = [0 for i in range(len(data))]
    cluster = []
    member = []
    iCluster = 0
    for i in range(len(data)):
        if marked[i] == 0:
            marked[i] = 1
            P, m = regionPts(i, data, minPts, maxPts, eps)
            if m == 0:
                noise[i] = 1
            else :
                cluster.append([i])
                member.append([m])
                marked, cluster, member, noise = dbScanCoreNested(P, data, minPts, maxPts, eps, marked, cluster, member, noise, iCluster)
                iCluster = iCluster + 1
    return cluster, member, noise

def dbScanCoreNested(P , data, minPts, maxPts, eps, marked, cluster, member, noise, iCluster):
    for i in range(len(P)):
        if marked[P[i]] == 1 and noise[P[i]] == 1:
            noise[P[i]] = 0
            cluster[iCluster].append(P[i])
            member[iCluster].append(0)
        elif marked[P[i]] == 0:
            marked[P[i]] = 1
            Px, mx = regionPts(P[i], data, minPts, maxPts, eps)
            if mx == 0:
                cluster[iCluster].append(P[i])
                member[iCluster].append(mx)
            else :
                cluster[iCluster].append(P[i])
                member[iCluster].append(mx)
                dbScanCoreNested(Px, data, minPts, maxPts, eps, marked, cluster, member, noise, iCluster)
    return marked, cluster, member, noise

def convertCluster(data, cluster):
    C = []
    for i in range(len(cluster)):
        C.append([])
        for j in range(len(cluster[i])):
            C[i].append(data[cluster[i][j]])
    return C

def convertNoise(data, noise):
    N = []
    for i in range(len(noise)):
        if noise[i] == 1:
            N.append(data[i])
    return N