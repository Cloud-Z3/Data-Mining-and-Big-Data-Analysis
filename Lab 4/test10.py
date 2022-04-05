import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import time

clusterAssment = None
labels = None


def loadDataset(infile):
    df = pd.read_csv(infile, sep=' ', header=None, dtype=str, na_filter=False)
    return np.array(df).astype(float)


# 计算欧氏距离
def calEDist(arrA, arrB):
    return np.math.sqrt(sum(np.power(arrA - arrB, 2)))


# 选择k个随机中心点
def randCent(data_X, k):
    n = data_X.shape[1]  # 获取特征的维数
    centroids = np.empty((k, n))  # 使用numpy生成一个k*n的矩阵，用于存储质心
    for j in range(n):
        x=data_X[:, j]
        minJ = min(data_X[:, j])    #选择data_X中第j列元素
        rangeJ = float(max(data_X[:, j] - minJ))
        centroids[:, j] = (minJ + rangeJ * np.random.rand(k, 1)).flatten()  # 使用flatten拉平嵌套列表
    return centroids


# 更新聚类中心点
def fit(data_X, k, maxiter, initCent):
    if not isinstance(data_X, np.ndarray) or isinstance(data_X, np.matrixlib.defmatrix.matrix):
        try:
            data_X = np.asarray(data_X)
        except:
            raise TypeError("numpy.ndarray resuired for data_X")
    m = data_X.shape[0]  # 获取样本的个数
    clusterAssment = np.zeros((m, 2))  # 一个m*2的二维矩阵，矩阵第一列存储样本点所属的索引值
    # 第二列存储该点与所属族的质心的平方误差
    if initCent == 'random':
        centroids = randCent(data_X, k)

    clusterChanged = True
    for _ in range(maxiter):
        clusterChanged = False
        for i in range(m):  # 将每个样本点分配到离它最近的质心所属的族
            minDist = np.inf  # 距最近质心的距离
            minIndex = -1  # 最近质心的下标
            for j in range(k):  # 次迭代用于寻找最近的质心，j为每个样本点的最近质心的下标，即第j个中心点
                arrA = centroids[j, :]  #中心点数组的第J行，即第J个中心点（0，1，2）
                arrB = data_X[i, :] #数据集的第i行（0，1，...，149）
                distJI = calEDist(arrA, arrB)  # 计算误差值
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i, 0] != minIndex or clusterAssment[i, 1] > minDist ** 2:
                clusterChanged = True
                clusterAssment[i, :] = minIndex, minDist ** 2
        if not clusterChanged:  # 若所有样本点所属的族都不改变，则已收敛，结束迭代
            break
        for i in range(k):  # 更新质心，将每个族中的点的均值作为质心
            index_all = clusterAssment[:, 0]  # 取出样本所属族的索引值
            value = np.nonzero(index_all == i)  # 取出所有属于第i个族的索引值
            ptsInClust = data_X[value[0]]  # 取出所有属于第i个族的所有样本点
            centroids[i, :] = np.mean(ptsInClust, axis=0)  # 计算均值
    labels = clusterAssment[:, 0]
    return centroids, labels


if __name__ == "__main__":
    data_X = loadDataset("E:\\Jerry\\My University\\大学\\课程\\第四学期\\数据挖掘\\实验4\\data.txt")
    k = 3
    maxiter = 500
    initCent = 'random'
    # clf = KMeansCluster(k)
    clf = fit(data_X, k, maxiter, initCent)
    cents = clf[0]
    labels = clf[1]

    colors = ['b', 'g', 'r', 'k', 'c', 'm', 'y', '#e24fff', '#524C90', '#845868']
    for i in range(k):
        index = np.nonzero(labels == i)[0]
        x0 = data_X[index, 0]
        x1 = data_X[index, 1]
        y_i = i
        for j in range(len(x0)):
            plt.text(x0[j], x1[j], str(y_i), color=colors[i], fontdict={'weight': 'bold', 'size': 6})
            plt.scatter(cents[i, 0], cents[i, 1], marker='x', color=colors[i], linewidths=7)
    plt.axis([-7, 7, -7, 7])
    plt.show()
