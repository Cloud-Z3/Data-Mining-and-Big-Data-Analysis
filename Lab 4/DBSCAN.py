import numpy as np
import matplotlib.pyplot as plt
import math
import time

UNCLASSIFIFD = False
NOISE = 0

def loadDataSet(fileName):                             #读取数据
    f = open(fileName)                                 #打开文件夹
    dataSet = []                                       #数据集初始化
    for i in f:
        a = i.split()                                  #将一行的两个数据分隔开
        dataSet.append([eval(a[0]), eval(a[1])])       #字符串转数字并存储点坐标
    return dataSet

def dist(a, b):                                        #计算欧几里得距离
    return math.sqrt(np.power(a - b, 2).sum())

def eps_neighbor(a, b, eps):                           #判断a和b的距离是否满足eps阈值
    return dist(a, b) < eps

def region_query(data, pointId, eps):                  #找到点周围邻域半径里的相邻点序号
    nPoints = data.shape[1]                            #返回数据点个数
    seeds = []
    for i in range(nPoints):
        #print(i,data[:, i])
        if eps_neighbor(data[:, pointId], data[:, i], eps):
            seeds.append(i)
    return seeds

def expend_cluster(data, clusterResult, pointId, clusterId, eps, minPts):  #根据点序号扩大其所在的簇
    seeds = region_query(data, pointId, eps)           #返回pointId对应点周围所有在eps邻域内的点序号
    if len(seeds) < minPts:
        clusterResult[pointId] = NOISE
        return False                                   #考察该点密度大小，若太小则返回错误
    else:
        clusterResult[pointId] = clusterId             #否则，标记为该点的簇号
        for seedId in seeds:
            clusterResult[seedId] = clusterId          #且邻域内所有点都为同样簇号
        while len(seeds) > 0:
            currentPoint = seeds[0]
            queryResults = region_query(data, currentPoint, eps)   #返回邻域内所有点的临近点个数
            if len(queryResults) >= minPts:                        #考察邻域内所有点是否满足密度条件
                for i in range(len(queryResults)):
                    resultPoint = queryResults[i]                  #点序号
                    if clusterResult[resultPoint] == UNCLASSIFIFD: #未分类则划分类别
                        seeds.append(resultPoint)
                        clusterResult[resultPoint] = clusterId
                    elif clusterResult[resultPoint] == NOISE:      #噪声点
                        clusterResult[resultPoint] = clusterId
            seeds = seeds[1:]
        return True

def dbscan(data, eps, minPts):                                     #DBSCAN核心函数，调度其余函数
    clusterId = 1
    nPoints = data.shape[1]
    clusterResult = [UNCLASSIFIFD] * nPoints                       #初始化
    for pointId in range(nPoints):                                 #对每个点完成搜索
        #point = data[:, pointId]
        if clusterResult[pointId] == UNCLASSIFIFD:                 #如果该点未分类，则进入下一步判断
            if expend_cluster(data, clusterResult, pointId, clusterId, eps, minPts):
                clusterId = clusterId + 1
    return clusterResult, clusterId - 1

def plotFeature(data, clusters, clusterNum):                       #可视化
    matClusters = np.mat(clusters).transpose()
    fig = plt.figure()
    scatterColors = ['black', 'blue', 'green', 'yellow', 'red', 'purple', 'orange', 'brown']
    ax = fig.add_subplot(111)
    for i in range(clusterNum + 1):
        colorSytle = scatterColors[i % len(scatterColors)]
        subCluster = data[:, np.nonzero(matClusters[:, 0].A == i)]
        ax.scatter(subCluster[0, :].flatten().A[0], subCluster[1, :].flatten().A[0], c=colorSytle, s=50)

def main():
    dataSet = loadDataSet('data.txt')                 #读取数据
    dataSet = np.mat(dataSet).transpose()             #生成矩阵并转置，得到所有横坐标与纵坐标
    clusters, clusterNum = dbscan(dataSet, 8, 1)      #得到分好的簇及聚类簇数
    cnum=len(set(clusters))
    for i in range(cnum):
        l=[]
        for j in range(len(clusters)):
            if clusters[j]==i+1:
                l.append(j)
        x=[dataSet[0,j] for j in l]
        xm=sum(x)/len(x)
        y = [dataSet[1, j] for j in l]
        ym = sum(y) / len(y)
        print('第' + str(i + 1) + '个簇的中心点：')
        print([xm,ym])
        print('含有点数：' + str(len(l)))
        print('')
    print("cluster Numbers=", clusterNum)             #显示信息
    plotFeature(dataSet, clusters, clusterNum)        #绘图


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('finish all in %s' % str(end - start))     #显示用时
    plt.show()

