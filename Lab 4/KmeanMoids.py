from random import*
import matplotlib.pyplot as plt

def Kmeans(pointlist,k):                             #K均值聚类的核心函数
    expointlist=pointlist
    shuffle(expointlist)
    oldcenterpoint=expointlist[:k]                   #选取k个点作为初始中心点
    clusterpoint=cluster(oldcenterpoint,pointlist)   #根据旧中心点对点集进行簇划分
    newcenterpoint=centriod(clusterpoint)            #找到划分好的簇的新中心点
    while(oldcenterpoint!=newcenterpoint):           #当新旧中心点不一样时继续更新
        oldcenterpoint=newcenterpoint                #旧中心点
        clusterpoint=cluster(oldcenterpoint,pointlist)  #根据旧中心点对点集进行簇划分
        newcenterpoint=centriod(clusterpoint)        #新中心点
    lastcluster=clusterpoint
    return lastcluster                               #返回聚类结果

def cluster(center,pointlist):                       #根据中心点对点集进行簇划分
    distancelist=[]                                  #距离列表，记录每个点到不同中心的距离
    for i in range(len(pointlist)):
        distancei=[]
        for j in range(len(center)):
            distancei.append(distancebtp(pointlist[i],center[j]))
        distancelist.append(distancei)
    nearestpoint=[]                                  #最近点列表，记录点集中每个点的最近中心点序号
    for i in range(len(pointlist)):
        leastdisid=0
        for j in range(1,len(center)):
            if(distancelist[i][j]<distancelist[i][leastdisid]):
                leastdisid=j
        nearestpoint.append(leastdisid)
    clusterpoint=[]                                  #记录根据该次中心点时点集的簇划分
    for i in range(len(center)):
        clusterpointi=[]
        for j in range(len(pointlist)):
            if(nearestpoint[j]==i):
                clusterpointi.append(pointlist[j])
        clusterpoint.append(clusterpointi)
    #print('该次  聚类结果：',clusterpoint)
    return clusterpoint                              #返回根据该次中心点时点集的簇划分

def centriod(clusterpoint):                          #输入簇划分，返回k个均值点
    length=len(clusterpoint)
    centriodlist=[]                                  #中心点列表
    pointlist=[]
    for i in range(length):
        centriodi=[0,0]
        for j in range(len(clusterpoint[i])):
            centriodi[0]+=clusterpoint[i][j][0]
            centriodi[1]+=clusterpoint[i][j][1]
            pointlist.append(clusterpoint[i][j])
        centriodi[0]/=len(clusterpoint[i])          #x均值
        centriodi[1]/=len(clusterpoint[i])          #y均值
        centriodlist.append(centriodi)              #添加中心点
    newcenter=[]
    for i in range(length):
        distancei=distancebtp(centriodlist[i],pointlist[0])
        indexi=0
        for j in range(1,len(pointlist)):
            if(distancebtp(centriodlist[i],pointlist[j])<distancei):
                distancei=distancebtp(centriodlist[i],pointlist[j])
                indexi=j
        newcenter.append(pointlist[indexi])
        del pointlist[indexi]                      #若将注释去掉，则为k中心算法。k均值与k中心算法的差别也仅在于此
    return newcenter                               #返回给定簇划分时的新中心点

def distancebtp(point1,point2):                    #给定两点，计算欧几里得距离
    distance2=pow(point1[0]-point2[0],2)+pow(point1[1]-point2[1],2)
    return pow(distance2,0.5)

if(__name__=='__main__'):                          #主函数，读出文件数据，使用Kmeans算法，并画图

    f = open('data.txt')
    points = []
    for i in f:
        a = i.split()
        points.append([eval(a[0]), eval(a[1])])
    #文件数据读取，得到点集

    k=3
    colorlist = ['red', 'peru', 'gold', 'lawngreen', 'cyan', 'navy', 'purple', 'hotpink']   #颜色列表
    lastcluster = Kmeans(points, k)                                                         #Kmeans算法
    center=centriod(lastcluster)                                                            #聚类中心点
    #print(lastcluster)
    for i in range(len(lastcluster)):                                                       #不同簇使用不同颜色，绘图
        plt.scatter([lastcluster[i][j][0] for j in range(len(lastcluster[i]))],[lastcluster[i][j][1] for j in range(len(lastcluster[i]))],marker='*')
    plt.scatter([center[j][0] for j in range(len(center))],[center[j][1] for j in range(len(center))],marker='*',color='k')   #中心点绘制
    plt.show()                                                                              #展示图形
    for i in range(k):                                                                      #展示聚类结果
        print('第'+str(i+1)+'个簇的中心点：')
        print(center[i])
        print('含有点数：'+str(len(lastcluster[i])))
        print('')